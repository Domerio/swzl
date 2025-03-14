# lost_and_found_app/views.py
import logging
import os
import time
from datetime import datetime, timedelta

from django.contrib import messages  # 用于显示消息
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db.models import Count
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import LostAndFound, Bookmark, Notification
from .serializers import UserRegisterSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    获取CSRF令牌的视图
    """
    return JsonResponse({'csrfToken': get_token(request)})


@api_view(['POST'])
@permission_classes([AllowAny])
# @csrf_exempt  # 临时添加，仅用于测试
def register(request):
    try:
        # 打印请求数据以便调试
        logger.info("Registration request data: %s", request.data)
        logger.info("Request headers: %s", request.headers)
        logger.info("Content type: %s", request.content_type)

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            print("Data is valid, creating user...")
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            print("User created successfully:", user.username)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'role': user.role,
                'real_name': user.real_name,
                'message': '注册成功'
            }, status=status.HTTP_201_CREATED)
        print("Validation errors:", serializer.errors)
        return Response({
            'error': serializer.errors,
            'message': '注册数据验证失败'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        logger.error("Registration error: %s", str(e))
        logger.error("Traceback: %s", traceback.format_exc())
        return Response({
            'error': str(e),
            'message': '注册过程发生错误'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not all([username, password]):
            return Response({
                'error': '请提供用户名和密码'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证用户
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'role': user.role,
                'real_name': user.real_name,
                'message': '登录成功'
            })
        else:
            return Response({
                'error': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print("Login error:", str(e))
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FrontendView(TemplateView):
    template_name = 'frontend/index.html'  # 直接指向模板位置


# 用户注销视图
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        # 记录登出日志
        logger.info(f"用户登出: {request.user.username}")

        # 清除会话信息
        request.auth.delete()
        logout(request)
        messages.success(request, '已成功注销')  # 注销成功提示
        return redirect('frontend/index.html')  # 重定向到登录页面

    except Exception as e:
        logger.error(f"登出异常: {str(e)}")
        return Response({
            "code": 500,
            "message": "登出过程发生错误：" + str(e)
        })


# 失物登记视图
@login_required
def lost_item_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lost_time = request.POST.get('lost_time')
        lost_location = request.POST.get('lost_location')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        return JsonResponse({'success': True})
    return render(request, 'frontend/index.html')


# 招领登记视图
@login_required
def found_item_register(request):
    if request.method == 'POST':
        # 处理招领登记表单
        # 这里可以添加具体的招领登记逻辑，例如创建 FoundItem 对象并保存
        # 示例：
        # name = request.POST.get('name')
        # found_time = request.POST.get('found_time')
        # found_location = request.POST.get('found_location')
        # description = request.POST.get('description')
        # contact_info = request.POST.get('contact_info')
        # finder = request.user
        # FoundItem.objects.create(name=name, found_time=found_time, found_location=found_location, description=description, contact_info=contact_info, finder=finder)
        messages.success(request, '招领信息已成功登记')  # 登记成功提示
        return redirect('found_item_list')
    return render(request, 'frontend/found_item_register.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):
    try:
        user = request.user
        logger.info(f"User {user.username} requested dashboard data")
        # 获取用户发布的所有信息
        my_posts = LostAndFound.objects.filter(user=user).order_by('-created_at')[:5]
        logger.debug(f"Recent posts query result count: {my_posts.count()}")
        # 获取用户的收藏
        bookmarks = Bookmark.objects.filter(user=user).select_related('item').order_by('-created_at')[:5]
        # 获取最近7天的发布统计
        last_week = datetime.now() - timedelta(days=7)
        daily_stats = LostAndFound.objects.filter(
            user=user,
            created_at__gte=last_week
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(count=Count('id')).order_by('date')
        logger.debug(f"Daily stats SQL: {daily_stats.query}")
        # 获取未读消息
        unread_notifications = Notification.objects.filter(
            user=user,
            is_read=False
        ).order_by('-created_at')[:5]
        # 统计各种状态的信息数量
        status_stats = LostAndFound.objects.filter(user=user).values(
            'status'
        ).annotate(count=Count('id'))
        # 获取物品分类统计
        category_stats = LostAndFound.objects.filter(
            user=user
        ).values(
            'category__name'
        ).annotate(
            value=Count('id')
        )
        # 获取用户活动日期
        activity_dates = LostAndFound.objects.filter(
            user=user,
            created_at__gte=datetime.now() - timedelta(days=30)
        ).dates('created_at', 'day')
        # 输出返回信息
        # (1) 打印原始查询结果到服务器控制台
        logger.debug("<=============== 分类统计原始查询数据 ===============>")
        logger.debug(list(category_stats))
        logger.debug("<=============== 每日统计原始查询数据 ===============>")
        logger.debug(list(daily_stats))
        # (2) 打印最终返回的数据结构
        return_data = {
            'status': 'success',
            'data': {
                'recent_posts': [{
                    'id': post.id,
                    'title': post.title,
                    'status': post.get_status_display(),
                    'created_at': post.created_at,
                    'category': post.category.name if post.category else None
                } for post in my_posts],
                'bookmarks': [{
                    'id': bookmark.item.id,
                    'title': bookmark.item.title,
                    'status': bookmark.item.get_status_display(),
                    'created_at': bookmark.created_at
                } for bookmark in bookmarks],
                'daily_stats': list(daily_stats),
                'notifications': [{
                    'id': notif.id,
                    'content': notif.content,
                    'created_at': notif.created_at,
                    'type': notif.notification_type
                } for notif in unread_notifications],
                'status_summary': {
                    item['status']: item['count'] for item in status_stats
                },
                'category_stats': [{
                    'name': stat['category__name'] or '未分类',
                    'value': stat['value']
                } for stat in category_stats],
                'activity_dates': [date.strftime('%Y-%m-%d') for date in activity_dates],
                'unread_notifications': unread_notifications.count()
            }
        }

        logger.debug("最终返回数据预览:")
        logger.debug(return_data)
        return Response(return_data)  # ✅ 确保返回对应的数据
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}", exc_info=True)
        return Response({
            'error': '获取仪表盘数据失败',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    获取和更新用户资料
    """
    if request.method == 'GET':
        return Response({
            'username': request.user.username,
            'real_name': request.user.real_name,
            'role': request.user.role,
            'phone': request.user.phone,
            'avatar': request.user.avatar.url if request.user.avatar else None,
            'is_verified': request.user.is_verified
        })

    elif request.method == 'PUT':
        user = request.user
        data = request.data

        if 'real_name' in data:
            user.real_name = data['real_name']
        if 'phone' in data:
            user.phone = data['phone']

        user.save()
        return Response({
            'message': '个人资料更新成功',
            'real_name': user.real_name,
            'phone': user.phone,
            'avatar': user.avatar.url if user.avatar else None
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def upload_avatar(request):
    print(request.headers)  # 打印请求头
    print(request.data)  # 打印请求体
    logging.info(f"上传头像请求头: {dict(request.headers)}")
    try:
        if 'avatar' not in request.FILES:
            logging.warning("未检测到上传文件")
            return Response({'error': '请选择头像文件'}, status=400)

        avatar_file = request.FILES['avatar']
        user = request.user

        # 文件校验
        if avatar_file.content_type not in ['image/jpeg', 'image/png']:
            return Response({'error': '仅支持 JPG/PNG 格式'}, status=400)
        if avatar_file.size > 2 * 1024 * 1024:
            return Response({'error': '文件不得超过2MB'}, status=400)

        # 保存逻辑
        ext = os.path.splitext(avatar_file.name)[1]
        filename = f'avatars/{user.username}_{int(time.time())}{ext}'

        # 删除旧头像
        if user.avatar:
            try:
                default_storage.delete(user.avatar.name)
            except Exception as del_error:
                logger.error(f"旧头像删除失败: {str(del_error)}")

        # 存储新头像
        file_path = default_storage.save(filename, avatar_file)
        user.avatar = file_path
        user.save()
        return Response({
            'message': '上传成功',
            'avatar_url': user.avatar.url
        }, status=200)

    except Exception as e:
        logger.error(f"头像上传系统级错误: {str(e)}", exc_info=True)
        return Response({'error': '服务器处理文件时发生异常'}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """
    标记所有通知为已读
    """
    try:
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)

        return Response({
            'message': '已将所有通知标记为已读'
        })
    except Exception as e:
        logger.error(f"Mark notifications read error: {str(e)}")
        return Response({
            'error': '操作失败'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

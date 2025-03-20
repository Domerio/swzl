# lost_and_found_app/views.py
import logging
from datetime import datetime, timedelta

from django.contrib import messages  # 用于显示消息
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import LostAndFound, Bookmark, Notification, Category, Attachment
from .serializers import UserRegisterSerializer, LostItemSerializer, LostAndFoundDetailSerializer

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
def user_dashboard(request):
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
        total_posts = LostAndFound.objects.filter(user=user).count()
        total_bookmarks = Bookmark.objects.filter(user=user).count()
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
                    'item_type': post.category.item_type if post.category else None,  # 新增
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
                'unread_notifications': unread_notifications.count(),
                'total_posts': total_posts,
                'total_bookmarks': total_bookmarks
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
        # print(request.build_absolute_uri(request.user.avatar.url))
        return Response({
            'username': request.user.username,
            'real_name': request.user.real_name,
            'role': request.user.role,
            'phone': request.user.phone,
            'avatar': request.build_absolute_uri(request.user.avatar.url) if request.user.avatar else None,
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
            'avatar': user.avatar if user.avatar else None
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def upload_avatar(request):
    try:
        return Response({
            'status': 'success',
            'data': {
                'avatar_url': request.user.avatar.url if request.user.avatar else None,
            }
        })

    except Exception as e:
        logger.error(f"头像上传失败: {str(e)}")
        return Response(
            {'error': '头像上传失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


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


def get_lost_categories(request):
    categories = Category.objects.filter(item_type='lost').values('id', 'name')
    return JsonResponse(list(categories), safe=False)


def get_found_categories(request):
    categories = Category.objects.filter(item_type='found').values('id', 'name')
    return JsonResponse(list(categories), safe=False)


@api_view(['GET'])
@permission_classes([AllowAny])  # 根据需要调整权限设置
def get_category_name(request, category_id):
    """
    获取指定分类ID的名称
    """
    try:
        category = Category.objects.get(id=category_id)
        return Response({
            'id': category.id,
            'name': category.name
        })
    except Category.DoesNotExist:
        logger.error(f"Category with ID {category_id} does not exist")
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error getting category name: {str(e)}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def item_detail(request, item_id):
    try:
        logger.info(f"Received request for item with ID: {item_id}")
        item = LostAndFound.objects.get(id=item_id)
        serializer = LostItemSerializer(item)
        logger.info(f"Item details: {serializer.data}")

        # 查询与该物品关联的所有图片
        attachments = Attachment.objects.filter(item=item)
        image_urls = [attachment.image.url for attachment in attachments]

        # 将图片信息添加到返回的数据中
        response_data = serializer.data
        response_data['images'] = image_urls

        return Response(response_data)
    except LostAndFound.DoesNotExist:
        logger.error(f"Item with ID {item_id} does not exist")
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error retrieving item details: {str(e)}")
        return Response({'error': 'An error occurred while retrieving item details'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_stats(request):
    if request.user.role == 'admin':
        pending_count = LostAndFound.objects.filter(status='pending').count()
        active_count = LostAndFound.objects.filter(status='active').count()
        completed_count = LostAndFound.objects.filter(status='completed').count()

        return Response({
            'pending_count': pending_count,
            'active_count': active_count,
            'completed_count': completed_count
        })
    else:
        return Response({'error': 'You are not authorized to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_recent_posts(request):
    if request.user.role == 'admin':
        recent_posts = LostAndFound.objects.order_by('-created_at')[:5]
        data = [{
            'id': post.id,
            'title': post.title,
            'status': post.status,
            'category': post.category.name if post.category else None,
            'item_type': post.category.item_type if post.category else None  # 新增
        } for post in recent_posts]

        return Response({
            'recent_posts': data
        })
    else:
        return Response({'error': 'You are not authorized to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_recent_users(request):
    if request.user.role == 'admin':
        recent_users = User.objects.order_by('-date_joined')[:5]
        data = [{
            'id': user.id,
            'username': user.username,
            'real_name': user.real_name,
            'role': user.role,
            'avatar': user.avatar.url if user.avatar else None
        } for user in recent_users]
        return Response({
            'recent_users': data
        })
    else:
        return Response({'error': 'You are not authorized to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)


# 在views.py中修改admin_item_detail视图
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_item_detail(request, item_id):
    try:
        item = LostAndFound.objects.select_related('user').prefetch_related('attachments').get(id=item_id)
        serializer = LostAndFoundDetailSerializer(item)  # 使用包含附件的详细序列化器
        return Response(serializer.data)
    except LostAndFound.DoesNotExist:
        return Response({'error': '物品不存在'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_user_detail(request, user_id):
    if not request.user.is_superuser:
        return Response({'error': '权限不足'}, status=403)

    try:
        user = User.objects.get(id=user_id)
        data = {
            'id': user.id,
            'username': user.username,
            'real_name': user.real_name,
            'role': user.role,
            'phone': user.phone,
            'email': user.email,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'is_active': user.is_active
        }
        return Response(data)
    except User.DoesNotExist:
        return Response({'error': '用户不存在'}, status=404)


# 新增状态更新接口
# 增加请求方法校验和日志记录
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_item_status(request, item_id):
    try:
        logger.info(f"开始处理状态更新请求，物品ID: {item_id}")
        logger.debug(f"请求用户: {request.user.username}，请求数据: {request.data}")

        item = LostAndFound.objects.get(id=item_id)

        # 权限校验增强
        if item.user != request.user and request.user.role != 'admin':
            logger.warning(f"用户{request.user.id}无权限修改物品{item_id}")
            return Response({'error': '无操作权限'}, status=status.HTTP_403_FORBIDDEN)

        # 强制只更新状态字段
        new_status = request.data.get('status')
        if new_status not in ['completed', 'active']:
            return Response({'error': '无效状态值'}, status=400)

        item.status = new_status
        item.save()

        logger.info(f"物品状态更新成功，ID: {item_id} 新状态: {new_status}")
        return Response({
            'status': 'success',
            'data': LostItemSerializer(item).data
        })

    except LostAndFound.DoesNotExist:
        logger.error(f"物品不存在，ID: {item_id}")
        return Response({'error': '物品不存在'}, status=404)
    except Exception as e:
        logger.error(f"状态更新异常: {str(e)}", exc_info=True)
        return Response({'error': '服务器内部错误'}, status=500)


# 新增专门的管理员审核接口
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_approve_item(request, item_id):
    logger.info(f"管理员审批请求 - 用户: {request.user.id} 物品: {item_id}")

    try:
        item = LostAndFound.objects.select_related('user').get(id=item_id)

        # 校验状态合法性
        if item.status != 'pending':
            return Response(
                {"error": "非待审状态物品无法操作"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 处理审批逻辑
        item.status = 'active'
        item.admin_operator = request.user
        item.review_time = timezone.now()
        item.save()

        # 发站内通知给提交者
        Notification.objects.create(
            user=item.user,
            content=f"您提交的 {item.title} 已通过审核",
            notification_type='system',
            related_item_id=item.id,
        )

        return Response(LostAndFoundDetailSerializer(item).data)

    except LostAndFound.DoesNotExist:
        logger.error(f"审批目标不存在: {item_id}")
        return Response(
            {"error": "目标物品不存在"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"审批过程异常: {str(e)}", exc_info=True)
        return Response(
            {"error": "审批过程中发生系统错误"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

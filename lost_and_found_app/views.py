# lost_and_found_app/views.py
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # 用于显示消息
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from django.middleware.csrf import get_token
import logging

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
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, '已成功注销')  # 注销成功提示
    return redirect('frontend/login.html')  # 重定向到登录页面


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
    return render(request, 'frontend/lost_item_register.html')


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

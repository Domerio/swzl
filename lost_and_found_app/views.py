# lost_and_found_app/views.py
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .forms import UserRegistrationForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # 用于显示消息
from django.views.decorators.csrf import csrf_exempt
import json


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # 注册成功后重定向到登录页面或其他页面
            # return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'frontend/register.html', {'form': form})


# 用户登录视图
@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 获取用户输入的用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"接收的 username: {username}, password: {password}")  # 确认字段正确
        # 验证用户输入的用户名和密码
        user = authenticate(request, username=username, password=password)
        print(f"用户对象：{user}")

        if user is not None:
            # 若用户验证成功，登录用户并重定向到首页
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('lost_and_found:home')  # 这里的 'home' 是你定义的首页 URL 名称
        else:
            # 若用户验证失败，显示错误消息
            messages.error(request, '用户名或密码错误，请重试。')
    return render(request, 'frontend/login.html')


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

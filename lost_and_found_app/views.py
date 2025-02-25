from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # 用于显示消息
from django.views.decorators.csrf import csrf_exempt
import json


# 用户注册视图
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            real_name = data.get('real_name')
            role = data.get('role')

            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': '学号/工号已存在，请使用其他学号/工号。', 'redirect_url': ''})

            # 创建用户对象
            user = User.objects.create_user(username=username, password=password, real_name=real_name, role=role)
            user.save()

            messages.success(request, '注册成功，请登录')  # 注册成功提示
            return JsonResponse({'success': True, 'message': '注册成功，请登录', 'redirect_url': '/login/'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'注册失败: {str(e)}', 'redirect_url': ''})
    return render(request, 'register.html')


# 用户登录视图
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return JsonResponse({'success': True, 'message': '登录成功', 'redirect_url': next_url})
                else:
                    return JsonResponse({'success': True, 'message': '登录成功', 'redirect_url': '/home/'})
            else:
                # 登录失败处理
                return JsonResponse({'success': False, 'message': '用户名或密码错误，请重试。', 'redirect_url': ''})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'登录失败: {str(e)}', 'redirect_url': ''})
    return render(request, 'login.html')


# 用户注销视图
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, '已成功注销')  # 注销成功提示
    return redirect('login')


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
    return render(request, 'lost_item_register.html')


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
    return render(request, 'found_item_register.html')


# 失物列表视图


# 招领列表视图
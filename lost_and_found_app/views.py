from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # 用于显示消息


# 用户注册视图
def register(request):
    if request.method == 'POST':
        # 处理注册表单
        # 这里可以添加具体的注册逻辑，例如创建用户对象等
        # 示例：
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # 进行用户创建和保存操作
        messages.success(request, '注册成功，请登录')  # 注册成功提示
        return redirect('login')
    return render(request, 'register.html')


# 用户登录视图
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)  # 重定向到 next 参数指定的页面
            else:
                return redirect('home')  # 如果没有 next 参数，重定向到首页
        else:
            # 登录失败处理
            messages.error(request, '用户名或密码错误，请重试。')
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

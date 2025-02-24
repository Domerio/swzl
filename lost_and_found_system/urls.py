from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# 定义一个视图函数，用于重定向到登录页面
def home_redirect(request):
    return redirect('lost_and_found:register')

urlpatterns = [
    path('admin/', admin.site.urls),
    # 包含 lost_and_found_app 应用的路由，并设置命名空间
    path('lost_and_found/', include('lost_and_found_app.urls', namespace='lost_and_found')),
    # 根路径重定向到注册页面
    path('', home_redirect, name='home'),
]
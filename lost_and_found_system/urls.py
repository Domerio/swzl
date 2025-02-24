from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include


# 定义一个视图函数，用于重定向到首页
def home_redirect(request):
    return redirect('lost_item_register')


# 定义项目的 URL 模式
urlpatterns = [
    path('admin/', admin.site.urls),  # 管理员后台页面
    path('', home_redirect, name='home'),  # 根路径重定向到丢失物品登记页面
    path('app/', include('lost_and_found_app.urls')),  # 包含应用的 URL 配置，将所有应用内的 URL 放在 /app/ 下
]

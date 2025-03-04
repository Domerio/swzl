# lost_and_found_app/urls.py
from django.urls import path, re_path

from . import views
from .views import register, login, user_logout, lost_item_register, found_item_register

# 添加 app_name 变量
app_name = 'lost_and_found'

urlpatterns = [
    # 用户注册视图路由
    path('register/', register, name='register'),
    # 用户登录视图路由
    path('login/', login, name='login'),
    # 用户注销视图路由
    path('logout/', user_logout, name='logout'),
    # 失物登记视图路由
    path('lost-item-register/', lost_item_register, name='lost_item_register'),
    # 招领登记视图路由
    path('found-item-register/', found_item_register, name='found_item_register'),
]

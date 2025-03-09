# lost_and_found_app/urls.py
from django.urls import path
from . import views

app_name = 'lost_and_found_app'

urlpatterns = [
    # 认证相关
    path('api/login/', views.login, name='login'),
    path('api/register/', views.register, name='register'),
    path('api/logout/', views.user_logout, name='logout'),
    
    # 页面路由
    path('lost-item-register/', views.lost_item_register, name='lost_item_register'),
    path('found-item-register/', views.found_item_register, name='found_item_register'),
]

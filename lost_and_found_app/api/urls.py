# lost_and_found_app/api/urls.py

from django.urls import path

from .views.auth import LoginAPI
from .views.auth import RegisterAPI
from .views.items import LostAndFoundListCreateAPI  # 确保导入路径正确
from .. import views

urlpatterns = [
    # ✅ 所有路径继承主项目层的 /api/ 前缀 → 完整路径为 /api/dashboard/
    path('dashboard/', views.student_dashboard, name='student-dashboard'),
    path('login/', LoginAPI.as_view(), name='login_api'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('items/', LostAndFoundListCreateAPI.as_view(), name='items'),
    # 用户资料
    path('user/profile/', views.user_profile, name='user-profile'),
    path('user/upload-avatar/', views.upload_avatar, name='upload-avatar'),
    path('user/notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    # 认证相关端点
    path('logout/', views.user_logout, name='logout'),
    path('csrf-token/', views.get_csrf_token, name='get-csrf-token'),
]

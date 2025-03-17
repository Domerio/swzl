# lost_and_found_app/api/urls.py

from django.urls import path

from .views.auth import LoginAPI, UploadAvatar
from .views.auth import RegisterAPI
from .views.items import LostItemCreateAPI  # 确保导入路径正确
from .. import views
from ..views import get_categories

urlpatterns = [
    # ✅ 所有路径继承主项目层的 /api/ 前缀 → 完整路径为 /api/dashboard/
    path('dashboard/', views.user_dashboard, name='user-dashboard'),
    path('login/', LoginAPI.as_view(), name='login_api'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('user/upload-avatar/', UploadAvatar.as_view(), name='upload_avatar'),
    path('categories/', get_categories, name='categories'),
    # path('items/', LostAndFoundListCreateAPI.as_view(), name='items'),
    path('items/lost/', LostItemCreateAPI.as_view(), name='lost_items'),
    path('items/:id/', views.item_detail, name='item-detail'),
    # 用户资料
    path('user/profile/', views.user_profile, name='user-profile'),
    # path('user/upload-avatar/', views.upload_avatar, name='upload-avatar'),
    path('user/notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    # 认证相关端点
    path('logout/', views.user_logout, name='logout'),
    path('csrf-token/', views.get_csrf_token, name='get-csrf-token'),
]

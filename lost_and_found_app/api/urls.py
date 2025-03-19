# lost_and_found_app/api/urls.py

from django.urls import path

from .views.auth import LoginAPI, UploadAvatar
from .views.auth import RegisterAPI
from .views.items import LostItemCreateAPI, FoundItemCreateAPI  # 确保导入路径正确
from .. import views

urlpatterns = [
    # ✅ 所有路径继承主项目层的 /api/ 前缀
    path('dashboard/', views.user_dashboard, name='user-dashboard'),
    path('login/', LoginAPI.as_view(), name='login_api'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('user/upload-avatar/', UploadAvatar.as_view(), name='upload_avatar'),
    path('lost/categories/', views.get_lost_categories, name='lost_categories'),
    path('found/categories/', views.get_found_categories, name='found_categories'),
    path('category/name/<int:category_id>/', views.get_category_name, name='category-name'),
    path('items/lost/', LostItemCreateAPI.as_view(), name='lost_items'),
    path('items/found/', FoundItemCreateAPI.as_view(), name='found_items'),
    path('items/<int:item_id>/', views.item_detail, name='item-detail'),
    path('user/items/<int:item_id>/status/', views.update_item_status, name='update-item-status'),
    path('admin/items/<int:item_id>/status/', views.admin_approve_item),

    # 用户资料
    path('user/profile/', views.user_profile, name='user-profile'),
    # path('user/upload-avatar/', views.upload_avatar, name='upload-avatar'),
    path('user/notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    path('admin/stats/', views.admin_stats, name='admin_stats'),
    path('admin/recent-posts/', views.admin_recent_posts, name='admin_recent_posts'),
    path('admin/recent-users/', views.admin_recent_users, name='admin_recent_users'),
    path('admin/found-items/<int:item_id>/', views.admin_item_detail, name='admin_items'),
    path('admin/users/<int:user_id>/', views.admin_user_detail, name='admin_users'),

    # 认证相关端点
    path('logout/', views.user_logout, name='logout'),
    path('csrf-token/', views.get_csrf_token, name='get-csrf-token'),
]

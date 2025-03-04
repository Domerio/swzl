# lost_and_found_app/api/urls.py
from django.urls import path
from .views.auth import RegisterAPI
from .views.items import LostAndFoundListCreateAPI  # 确保导入路径正确
from .views.auth import LoginAPI

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login_api'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('items/', LostAndFoundListCreateAPI.as_view(), name='items'),
]

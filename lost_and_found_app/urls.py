# lost_and_found_app/urls.py

from django.urls import path

from . import views

app_name = 'lost_and_found_app'

urlpatterns = [
    # 页面路由
    path('lost-item-register/', views.lost_item_register, name='lost_item_register'),
    path('found-item-register/', views.found_item_register, name='found_item_register'),
]

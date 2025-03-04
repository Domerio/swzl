# frontend/urls.py
from django.urls import re_path
from lost_and_found_app import views

urlpatterns = [
    re_path(r'^.*$', views.FrontendView.as_view())
]
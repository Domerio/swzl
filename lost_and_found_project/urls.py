# lost_and_found_project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from lost_and_found_app import views as frontend_views


# 定义一个视图函数，用于重定向到登录页面
def login(request):
    return redirect('lost_and_found:login')


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include('lost_and_found_app.api.urls')),  # 包含api路由
    # 推荐使用独立的前端路径
    # re_path(r'^', include('frontend.urls'))
    re_path(r'^(?!static/|media/|api/).*', frontend_views.FrontendView.as_view(), name='frontend')
]

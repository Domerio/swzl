# lost_and_found_project/urls.py
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from lost_and_found_project import settings

# 定义一个视图函数，用于重定向到登录页面
# def login(request):
#     return redirect('lost_and_found:login')


urlpatterns = [
    path('api/', include('lost_and_found_app.api.urls')),  # 包含api路由
    path('user/', include('lost_and_found_app.urls')),  # 普通页面路由入口
    # → 明确的前后端分离模式 ↓
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
# ONLY IN DEBUG MODE
if settings.DEBUG:
    # 生产环境下应禁用此路由
    urlpatterns += [
        re_path(r'^.*$', TemplateView.as_view(template_name='frontend/index.html'))  # 确保它始终在最后
    ]
# 开发环境静态文件服务
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

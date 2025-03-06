# lost_and_found_project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.views.generic import TemplateView
from lost_and_found_app import views as frontend_views
from lost_and_found_project import settings
from django.conf.urls.static import static


# 定义一个视图函数，用于重定向到登录页面
def login(request):
    return redirect('lost_and_found:login')


urlpatterns = [
                  # path('admin/', admin.site.urls),
                  path('api/', include('lost_and_found_app.api.urls')),  # 包含api路由
                  re_path(r'^.*$', TemplateView.as_view(template_name='frontend/index.html')),
              ]

# 仅在开发模式下启用静态文件服务
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 如果有媒体文件

from django.urls import path, include

urlpatterns = [
    path('api/', include('lost_and_found_app.api.urls')),  # 指向api子路由
]

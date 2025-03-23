from rest_framework import generics, permissions
from rest_framework.response import Response
from ...models import Notification
from...serializers import NotificationSerializer

class NotificationListAPI(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

class MarkNotificationReadAPI(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        return self.handle_request(request, **kwargs)
        
    def patch(self, request, *args, **kwargs):
        return self.handle_request(request, **kwargs)
        
    def handle_request(self, request, **kwargs):  # 必须添加**kwargs参数
        notification_id = kwargs.get('pk')
        try:
            notification = Notification.objects.get(
                id=notification_id,
                user=request.user,
                is_read=False  # 添加过滤条件避免重复操作
            )
            notification.is_read = True
            notification.save()
            return Response({'status': 'success'})
        except Notification.DoesNotExist:
            return Response({'error': '通知不存在或已被处理'}, status=404)
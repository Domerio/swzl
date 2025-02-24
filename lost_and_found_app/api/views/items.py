# lost_and_found_app/api/views/items.py
from rest_framework import generics
from rest_framework import permissions  # 添加此行
from ...models import LostAndFound
from ...serializers import LostAndFoundSerializer


class LostAndFoundListCreateAPI(generics.ListCreateAPIView):
    serializer_class = LostAndFoundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LostAndFound.objects.filter(status='active')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

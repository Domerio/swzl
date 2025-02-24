# lost_and_found_app/api/views/auth.py
from rest_framework import generics
from rest_framework.response import Response
from ...serializers import UserSerializer
from ...models import User


class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        return Response({"user_id": user.id})


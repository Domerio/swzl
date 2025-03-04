# lost_and_found_app/api/views/auth.py
from rest_framework import generics
from rest_framework.response import Response
from ...serializers import UserSerializer
from ...models import User

from rest_framework.views import APIView
from rest_framework.response import Response


class LoginAPI(APIView):
    def post(self, request):
        # 处理登录逻辑
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            # 登录成功，返回用户信息
            return Response({"message": "Login successful", "user": UserSerializer(user).data})
        else:
            # 登录失败，返回错误信息
            return Response({"message": "Invalid username or password"})


class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        return Response({"user_id": user.id})

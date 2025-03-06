# lost_and_found_app/api/views/auth.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from ...serializers import UserSerializer
from ...models import User
import logging
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)


class CustomAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        # ✅ 关键：首先调用父类验证逻辑以获取用户信息
        attrs = super().validate(attrs)
        user = attrs['user']  # 正确获取用户实例
        token, created = Token.objects.get_or_create(user=user)  # 此处生成Token

        return {
            # ✔️ 返回视图所需的全部信息
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'role': user.role,
            # 'user': user  # 关键! 保持父类结构兼容性
            'real_name': user.real_name,
        }


class LoginAPI(ObtainAuthToken):  # 核心：继承正确的基类
    serializer_class = CustomAuthTokenSerializer  # ✅ 绑定序列化器

    def post(self, request, *args, **kwargs):
        # ✔️ 直接使用序列化器生成的数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)  # ← 所有数据已在序列化器生成


class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        return Response({"user_id": user.id})

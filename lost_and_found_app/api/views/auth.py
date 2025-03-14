# lost_and_found_app/api/views/auth.py
import logging

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from ...models import User
from ...serializers import UserRegisterSerializer

logger = logging.getLogger(__name__)


class CustomAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        # ✅ 关键：首先调用父类验证逻辑以获取用户信息
        # 调用父类的validate方法，进行基本的验证逻辑，并返回验证后的属性字典
        attrs = super().validate(attrs)
        # 从验证后的属性字典中获取用户实例
        user = attrs['user']  # 正确获取用户实例
        # 使用Django的Token模型为用户生成或获取一个Token
        # Token.objects.get_or_create(user=user)会尝试获取用户已有的Token，如果没有则创建一个新的Token
        token, created = Token.objects.get_or_create(user=user)  # 此处生成Token

        # 返回一个包含视图所需全部信息的字典
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
    serializer_class = UserRegisterSerializer  # 修改为 UserRegisterSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'role': user.role,
            'real_name': user.real_name,
            'message': '注册成功'
        }, status=status.HTTP_201_CREATED)

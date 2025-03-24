# lost_and_found_app/api/views/auth.py
import logging
import time

from django.core.files.storage import default_storage
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import User
from ...serializers import UserRegisterSerializer

logger = logging.getLogger(__name__)


class CustomAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = attrs['user']
        
        # 新增：更新最后登录时间
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        token, created = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'role': user.role,
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


class UploadAvatar(APIView):
    def post(self, request, *args, **kwargs):
        # 输出请求检查
        print(request)
        print(request.FILES)
        if 'file' not in request.FILES:
            return Response(
                {'error': '没有上传文件'},
                status=status.HTTP_400_BAD_REQUEST
            )
        avatar_file = request.FILES['file']

        # 检查上传的文件是否为图片类型
        if not avatar_file.content_type.startswith('image/'):
            # 如果文件类型不是以'image/'开头，说明不是图片文件
            return Response(
                {'error': '请上传图片文件'},  # 返回一个包含错误信息的响应体
                status=status.HTTP_400_BAD_REQUEST  # 设置响应状态码为400，表示客户端请求错误
            )

        # 生成文件名
        timestamp = int(time.time())
        filename = f'avatars/{request.user.id}_{timestamp}_{avatar_file.name}'

        # 保存文件
        file_path = default_storage.save(filename, avatar_file)

        # 更新用户头像
        request.user.avatar = file_path
        request.user.save()
        # 处理头像上传的逻辑
        return Response({
            "status": "success",
            "data": {
                'avatar_url': request.build_absolute_uri(request.user.avatar.url)
            }
        }, status=status.HTTP_200_OK)

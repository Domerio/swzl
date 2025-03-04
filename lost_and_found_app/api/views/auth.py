# lost_and_found_app/api/views/auth.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import AllowAny

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



class LoginAPI(APIView):
    permission_classes = [AllowAny]  # 允许无需认证的访问
    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Step 1: 用户认证
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=401)

        # Step 2: 获取或创建用户 Token
        token, created = Token.objects.get_or_create(user=user)

        # Step 3: 返回 Token 和用户信息
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=200)


class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        return Response({"user_id": user.id})

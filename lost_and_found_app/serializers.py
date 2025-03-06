# lost_and_found_app/serializers.py
from contextvars import Token

from flask import Response
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from .models import User, Category
# from .models.item import LostAndFound


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        if not User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("用户名不存在")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'real_name', 'role', 'phone', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}  # 密码字段仅写

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LostAndFoundSerializer(serializers.ModelSerializer):
    class Meta:
        from .models.item import LostAndFound
        model = LostAndFound
        fields = '__all__'
        read_only_fields = ['user', 'status']  # 用户和状态不可修改


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# lost_and_found_app/serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User, Category, Notification

# from .models.item import LostAndFound

User = get_user_model()


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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'real_name', 'role', 'phone', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'real_name': {'required': True},
            'role': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
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


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'real_name', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'real_name': {'required': True},
            'role': {'required': True}
        }

    def validate(self, data):
        # 验证密码匹配
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次输入的密码不一致'})

        # 验证用户名是否已存在
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': '该用户名已被注册'})

        return data

    def create(self, validated_data):
        # 移除确认密码字段
        validated_data.pop('confirm_password')

        # 创建用户
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            real_name=validated_data['real_name'],
            role=validated_data['role']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('请提供用户名和密码')

        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'content', 'notification_type', 'is_read', 'created_at']


class CategoryStatsSerializer(serializers.ModelSerializer):
    total_items = serializers.IntegerField()
    active_items = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'total_items', 'active_items']

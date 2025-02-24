from rest_framework import serializers
from .models import User, LostAndFound, Category


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
        model = LostAndFound
        fields = '__all__'
        read_only_fields = ['user', 'status']  # 用户和状态不可修改


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

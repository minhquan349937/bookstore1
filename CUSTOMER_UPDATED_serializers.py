# api/serializers.py - CUSTOMER SERVICE (Updated with Auth)

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Customer

class UserSerializer(serializers.ModelSerializer):
    """Serializer cho User registration"""
    
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password_confirm',
            'phone',
            'address',
            'city',
            'postal_code',
            'country',
            'date_of_birth',
            'is_verified'
        ]
        read_only_fields = ['id', 'is_verified']
    
    def validate(self, data):
        """Kiểm tra password match"""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Mật khẩu không khớp"})
        return data
    
    def create(self, validated_data):
        """Tạo user mới"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer cho User login"""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Xác thực thông tin đăng nhập"""
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        
        if not user:
            raise serializers.ValidationError("Tên đăng nhập hoặc mật khẩu không đúng")
        
        data['user'] = user
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer cho User detail"""
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'city',
            'postal_code',
            'country',
            'date_of_birth',
            'avatar',
            'is_verified',
            'total_orders',
            'total_spent',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'total_orders', 'total_spent', 'created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer cho Customer profile"""
    
    user = UserDetailSerializer(read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id',
            'user',
            'tier',
            'loyalty_points',
            'favorite_books',
            'last_viewed_books',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

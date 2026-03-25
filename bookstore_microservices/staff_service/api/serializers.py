from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Staff

class StaffProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = Staff
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'phone', 'department', 'is_active']

class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class StaffRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=['admin', 'manager', 'librarian'], default='librarian')
    department = serializers.CharField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        # Extract staff-specific data
        role = validated_data.pop('role', 'librarian')
        phone = validated_data.pop('phone', '')
        department = validated_data.pop('department', '')
        
        # Check if user already exists
        if User.objects.filter(username=validated_data.get('username')).exists():
            raise serializers.ValidationError({'username': 'This username already exists'})
        
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError({'email': 'This email already exists'})
        
        # Create user
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create staff profile
        Staff.objects.create(
            user=user,
            role=role,
            phone=phone,
            department=department
        )
        
        return user

class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

# api/serializers.py - CUSTOMER SERVICE

from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer cho Model Customer"""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'address',
            'city',
            'postal_code',
            'country',
            'date_joined',
            'last_login',
            'is_active',
            'total_orders',
            'total_spent',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'date_joined', 
            'created_at', 
            'updated_at',
            'total_orders',
            'total_spent'
        ]
    
    def validate_email(self, value):
        """Kiểm tra email hợp lệ"""
        if Customer.objects.filter(email=value).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError("Email này đã được sử dụng")
        return value
    
    def validate_phone(self, value):
        """Kiểm tra số điện thoại"""
        if len(value) < 9 or len(value) > 15:
            raise serializers.ValidationError("Số điện thoại không hợp lệ")
        return value

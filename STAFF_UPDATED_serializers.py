# api/serializers.py - STAFF SERVICE

from rest_framework import serializers
from .models import StaffUser, Staff

class StaffUserSerializer(serializers.ModelSerializer):
    """Serializer cho StaffUser"""
    
    class Meta:
        model = StaffUser
        fields = [
            'id',
            'username',
            'email',
            'role',
            'phone',
            'department',
            'hire_date',
            'is_active_staff',
            'last_logged_in',
        ]
        read_only_fields = ['hire_date', 'last_logged_in']


class StaffProfileSerializer(serializers.ModelSerializer):
    """Serializer cho Staff profile"""
    
    user = StaffUserSerializer(read_only=True)
    
    class Meta:
        model = Staff
        fields = [
            'id',
            'user',
            'position',
            'salary',
            'address',
            'city',
            'country',
            'books_added',
            'books_edited',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'books_added',
            'books_edited',
            'created_at',
            'updated_at'
        ]

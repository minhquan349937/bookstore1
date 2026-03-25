# api/serializers.py - CART SERVICE

from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    """Serializer cho CartItem"""
    
    class Meta:
        model = CartItem
        fields = [
            'id',
            'book_id',
            'book_title',
            'book_author',
            'book_price',
            'quantity',
            'subtotal',
            'added_at',
            'updated_at'
        ]
        read_only_fields = ['subtotal', 'added_at', 'updated_at']
    
    def validate_quantity(self, value):
        """Kiểm tra số lượng"""
        if value < 1:
            raise serializers.ValidationError("Số lượng phải lớn hơn 0")
        if value > 100:
            raise serializers.ValidationError("Số lượng không thể vượt quá 100")
        return value


class CartSerializer(serializers.ModelSerializer):
    """Serializer cho Cart"""
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = [
            'id',
            'customer_id',
            'items',
            'total_items',
            'total_price',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'total_items',
            'total_price',
            'created_at',
            'updated_at'
        ]

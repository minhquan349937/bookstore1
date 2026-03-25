from rest_framework import serializers
from api.models import Cart, CartItem
from django.db.models import F, Sum

class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity', 'price', 'subtotal', 'added_at']
    
    def get_subtotal(self, obj):
        return float(obj.price) * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']
    
    def get_total_items(self, obj):
        return obj.items.aggregate(total=Sum('quantity'))['total'] or 0
    
    def get_total_price(self, obj):
        return sum([float(item.price) * item.quantity for item in obj.items.all()]) or 0

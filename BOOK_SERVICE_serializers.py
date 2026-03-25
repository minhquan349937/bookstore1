# books/serializers.py - BOOK SERVICE

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """Serializer cho Model Book"""
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'description',
            'genre',
            'price',
            'stock',
            'publication_date',
            'publisher',
            'pages',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_price(self, value):
        """Kiểm tra giá tiền phải dương"""
        if value <= 0:
            raise serializers.ValidationError("Giá tiền phải lớn hơn 0")
        return value
    
    def validate_stock(self, value):
        """Kiểm tra số lượng tồn kho"""
        if value < 0:
            raise serializers.ValidationError("Số lượng tồn kho không được âm")
        return value

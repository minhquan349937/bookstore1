# books/views.py - BOOK SERVICE

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho quản lý sách
    
    Cung cấp các API endpoints:
    - GET /api/books/ - Lấy danh sách tất cả sách
    - POST /api/books/ - Tạo sách mới
    - GET /api/books/{id}/ - Lấy chi tiết sách
    - PUT /api/books/{id}/ - Cập nhật sách
    - DELETE /api/books/{id}/ - Xóa sách
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """Hỗ trợ filter theo genre"""
        queryset = Book.objects.all()
        
        genre = self.request.query_params.get('genre', None)
        if genre is not None:
            queryset = queryset.filter(genre=genre)
        
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__icontains=author)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Lấy danh sách sách còn hàng"""
        available_books = self.get_queryset().filter(stock__gt=0)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def decrease_stock(self, request, pk=None):
        """Giảm số lượng tồn kho (khi bán sách)"""
        book = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if book.stock < quantity:
            return Response(
                {'error': 'Không đủ hàng trong kho'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.stock -= quantity
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increase_stock(self, request, pk=None):
        """Tăng số lượng tồn kho (khi nhập hàng)"""
        book = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        book.stock += quantity
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)

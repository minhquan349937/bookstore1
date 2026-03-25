# api/views.py - BOOK SERVICE (Updated with Staff Management & Search)

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho quản lý & tìm kiếm sách
    
    Endpoints:
    - GET /api/books/ - Danh sách sách (có phân trang & filter)
    - POST /api/books/ - Tạo sách (chỉ admin)
    - GET /api/books/{id}/ - Chi tiết sách
    - PUT /api/books/{id}/ - Cập nhật sách (chỉ admin)
    - DELETE /api/books/{id}/ - Xóa sách (chỉ admin)
    - GET /api/books/available/ - Sách còn hàng
    - GET /api/books/search/ - Tìm kiếm sách
    - POST /api/books/bulk_upload/ - Import sách hàng loạt
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'author', 'publisher']
    search_fields = ['title', 'author', 'isbn', 'description']
    ordering_fields = ['price', 'title', 'created_at', 'stock']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter sách dựa trên query parameters"""
        queryset = Book.objects.all()
        
        # Filter theo giá
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(price__lte=float(max_price))
        
        # Filter theo tồn kho
        in_stock_only = self.request.query_params.get('in_stock_only')
        if in_stock_only and in_stock_only.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Tìm kiếm sách nâng cao
        
        GET /api/books/search/?q=django&sort=price
        """
        
        query = request.query_params.get('q', '')
        sort = request.query_params.get('sort', 'title')
        
        if not query:
            return Response(
                {'error': 'Cần cung cấp từ khóa tìm kiếm (q)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tìm kiếm trong title, author, description
        books = Book.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(isbn__icontains=query)
        )
        
        # Sắp xếp
        if sort == 'price_asc':
            books = books.order_by('price')
        elif sort == 'price_desc':
            books = books.order_by('-price')
        elif sort == 'newest':
            books = books.order_by('-created_at')
        elif sort == 'popular':
            books = books.order_by('-stock')
        
        serializer = self.get_serializer(books, many=True)
        return Response({
            'count': books.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Lấy danh sách sách còn hàng"""
        available_books = self.get_queryset().filter(stock__gt=0)
        serializer = self.get_serializer(available_books, many=True)
        return Response({
            'count': available_books.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        """
        Lấy danh sách sách theo thể loại
        
        GET /api/books/by_genre/?genre=science
        """
        
        genre = request.query_params.get('genre')
        
        if not genre:
            genres = Book.objects.values_list('genre', flat=True).distinct()
            return Response({'available_genres': list(genres)})
        
        books = self.get_queryset().filter(genre=genre)
        serializer = self.get_serializer(books, many=True)
        return Response({
            'genre': genre,
            'count': books.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def decrease_stock(self, request, pk=None):
        """Giảm tồn kho (khi bán sách)"""
        book = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if book.stock < int(quantity):
            return Response(
                {'error': 'Không đủ hàng trong kho'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.stock -= int(quantity)
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increase_stock(self, request, pk=None):
        """Tăng tồn kho (khi nhập hàng)"""
        book = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        book.stock += int(quantity)
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_price(self, request, pk=None):
        """Cập nhật giá sách"""
        book = self.get_object()
        new_price = request.data.get('price')
        
        if not new_price or float(new_price) <= 0:
            return Response(
                {'error': 'Giá phải lớn hơn 0'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_price = book.price
        book.price = float(new_price)
        book.save()
        
        serializer = self.get_serializer(book)
        return Response({
            'message': f'Cập nhật giá từ {old_price} thành {new_price}',
            'book': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def update_all_info(self, request, pk=None):
        """
        Cập nhật tất cả thông tin sách
        
        POST /api/books/{id}/update_all_info/
        Body:
        {
            "title": "New Title",
            "author": "New Author",
            "price": 39.99,
            "stock": 25,
            "publication_date": "2023-01-01",
            "publisher": "New Publisher",
            "pages": 400
        }
        """
        
        book = self.get_object()
        
        # Cập nhật các fields nếu có
        for attr, value in request.data.items():
            if hasattr(book, attr):
                setattr(book, attr, value)
        
        book.save()
        serializer = self.get_serializer(book)
        return Response({
            'message': 'Cập nhật thành công',
            'book': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """
        Upload nhiều sách cùng lúc
        
        POST /api/books/bulk_upload/
        Body: [List of book objects]
        """
        
        data = request.data if isinstance(request.data, list) else [request.data]
        
        created_books = []
        errors = []
        
        for item in data:
            serializer = self.get_serializer(data=item)
            
            if serializer.is_valid():
                serializer.save()
                created_books.append(serializer.data)
            else:
                errors.append({
                    'book': item.get('title', 'Unknown'),
                    'errors': serializer.errors
                })
        
        return Response({
            'created_count': len(created_books),
            'error_count': len(errors),
            'created': created_books,
            'errors': errors
        }, status=status.HTTP_201_CREATED if errors == [] else status.HTTP_207_MULTI_STATUS)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Thống kê sách"""
        books = self.get_queryset()
        
        stats = {
            'total_books': books.count(),
            'total_stock': sum(b.stock for b in books),
            'total_value': sum(float(b.price) * b.stock for b in books),
            'genres': list(books.values('genre').distinct()),
            'average_price': sum(float(b.price) for b in books) / books.count() if books.count() > 0 else 0,
            'books_out_of_stock': books.filter(stock=0).count(),
        }
        
        return Response(stats)

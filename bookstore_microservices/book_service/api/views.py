from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search books by title or author"""
        query = request.query_params.get('q', '')
        if query:
            books = Book.objects.filter(title__icontains=query) | \
                    Book.objects.filter(author__icontains=query)
        else:
            books = Book.objects.all()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increase_stock(self, request, pk=None):
        """Increase book stock"""
        book = self.get_object()
        quantity = request.data.get('quantity', 1)
        book.stock += int(quantity)
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def decrease_stock(self, request, pk=None):
        """Decrease book stock"""
        book = self.get_object()
        quantity = request.data.get('quantity', 1)
        book.stock -= int(quantity)
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)

@api_view(['GET'])
def api_root(request):
    return Response({'message': 'Welcome to Book Service'})

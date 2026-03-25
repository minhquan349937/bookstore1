from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Laptop
from .serializers import LaptopSerializer

class LaptopViewSet(viewsets.ModelViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search laptops by name, brand, or model"""
        query = request.query_params.get('q', '')
        if query:
            laptops = Laptop.objects.filter(name__icontains=query) | \
                      Laptop.objects.filter(brand__icontains=query) | \
                      Laptop.objects.filter(model_name__icontains=query)
        else:
            laptops = Laptop.objects.all()
        serializer = self.get_serializer(laptops, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increase_stock(self, request, pk=None):
        """Increase laptop stock"""
        laptop = self.get_object()
        quantity = request.data.get('quantity', 1)
        laptop.stock += int(quantity)
        laptop.save()
        serializer = self.get_serializer(laptop)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def decrease_stock(self, request, pk=None):
        """Decrease laptop stock"""
        laptop = self.get_object()
        quantity = request.data.get('quantity', 1)
        laptop.stock -= int(quantity)
        laptop.save()
        serializer = self.get_serializer(laptop)
        return Response(serializer.data)

@api_view(['GET'])
def api_root(request):
    return Response({'message': 'Welcome to Laptop Service'})

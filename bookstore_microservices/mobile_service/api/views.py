from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Mobile
from .serializers import MobileSerializer

class MobileViewSet(viewsets.ModelViewSet):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search mobiles by name, brand, or model"""
        query = request.query_params.get('q', '')
        if query:
            mobiles = Mobile.objects.filter(name__icontains=query) | \
                      Mobile.objects.filter(brand__icontains=query) | \
                      Mobile.objects.filter(model_name__icontains=query)
        else:
            mobiles = Mobile.objects.all()
        serializer = self.get_serializer(mobiles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increase_stock(self, request, pk=None):
        """Increase mobile stock"""
        mobile = self.get_object()
        quantity = request.data.get('quantity', 1)
        mobile.stock += int(quantity)
        mobile.save()
        serializer = self.get_serializer(mobile)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def decrease_stock(self, request, pk=None):
        """Decrease mobile stock"""
        mobile = self.get_object()
        quantity = request.data.get('quantity', 1)
        mobile.stock -= int(quantity)
        mobile.save()
        serializer = self.get_serializer(mobile)
        return Response(serializer.data)

@api_view(['GET'])
def api_root(request):
    return Response({'message': 'Welcome to Mobile Service'})

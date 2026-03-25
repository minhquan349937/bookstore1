# api/views.py - CUSTOMER SERVICE

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho quản lý khách hàng
    
    Cung cấp các API endpoints:
    - GET /api/customers/ - Danh sách khách hàng
    - POST /api/customers/ - Tạo khách hàng mới
    - GET /api/customers/{id}/ - Chi tiết khách hàng
    - PUT /api/customers/{id}/ - Cập nhật khách hàng
    - DELETE /api/customers/{id}/ - Xóa khách hàng
    """
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        """Hỗ trợ filter theo trạng thái"""
        queryset = Customer.objects.all()
        
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        city = self.request.query_params.get('city', None)
        if city is not None:
            queryset = queryset.filter(city__icontains=city)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def top_customers(self, request):
        """Lấy danh sách 10 khách hàng chi tiêu nhiều nhất"""
        top_customers = self.get_queryset().order_by('-total_spent')[:10]
        serializer = self.get_serializer(top_customers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_last_login(self, request, pk=None):
        """Cập nhật thời gian đăng nhập cuối"""
        from django.utils import timezone
        customer = self.get_object()
        customer.last_login = timezone.now()
        customer.save()
        
        serializer = self.get_serializer(customer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_total_spent(self, request, pk=None):
        """Cập nhật tổng chi tiêu"""
        customer = self.get_object()
        amount = request.data.get('amount', 0)
        
        customer.total_spent += amount
        customer.total_orders += 1
        customer.save()
        
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

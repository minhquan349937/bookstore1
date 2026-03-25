# api/views.py - CUSTOMER SERVICE (Updated with Auth)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Customer
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    CustomerSerializer
)

class UserViewSet(viewsets.ViewSet):
    """
    ViewSet cho quản lý User Authentication
    
    Endpoints:
    - POST /api/users/register/ - Đăng ký tài khoản
    - POST /api/users/login/ - Đăng nhập
    - GET /api/users/profile/ - Xem profile
    - PUT /api/users/profile/ - Cập nhật profile
    - POST /api/users/logout/ - Đăng xuất
    """
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Đăng ký tài khoản mới
        
        POST /api/users/register/
        Body:
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "0912345678"
        }
        """
        
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.user_type = 'customer'
            user.save()
            
            # Tạo customer profile
            customer = Customer.objects.create(user=user)
            
            # Tạo token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Đăng ký thành công',
                'user': UserDetailSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Đăng nhập
        
        POST /api/users/login/
        Body:
        {
            "username": "john_doe",
            "password": "securepass123"
        }
        """
        
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Cập nhật last_login
            from django.utils import timezone
            user.last_login = timezone.now()
            user.save()
            
            # Lấy hoặc tạo token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'Đăng nhập thành công',
                'user': UserDetailSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Lấy thông tin profile của user hiện tại"""
        
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Cần đăng nhập'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """Cập nhật profile"""
        
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Cần đăng nhập'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = request.user
        
        # Cập nhật các fields
        for attr, value in request.data.items():
            if hasattr(user, attr) and attr != 'password':
                setattr(user, attr, value)
        
        user.save()
        serializer = UserDetailSerializer(user)
        return Response({
            'message': 'Cập nhật thành công',
            'user': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Đăng xuất"""
        
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Chưa đăng nhập'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Xóa token
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        return Response(
            {'message': 'Đăng xuất thành công'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Đổi mật khẩu
        
        POST /api/users/change_password/
        Body:
        {
            "old_password": "current_pass",
            "new_password": "new_pass",
            "new_password_confirm": "new_pass"
        }
        """
        
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Cần đăng nhập'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        
        # Kiểm tra mật khẩu cũ
        if not user.check_password(old_password):
            return Response(
                {'error': 'Mật khẩu cũ không đúng'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Kiểm tra mật khẩu mới khớp
        if new_password != new_password_confirm:
            return Response(
                {'error': 'Mật khẩu mới không khớp'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cập nhật mật khẩu
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Đổi mật khẩu thành công'
        })


class CustomerViewSet(viewsets.ViewSet):
    """
    ViewSet cho Customer profile mở rộng
    
    Endpoints:
    - GET /api/customers/{user_id}/ - Lấy profile
    - PUT /api/customers/{user_id}/ - Cập nhật profile
    - POST /api/customers/{user_id}/add_to_favorites/ - Thêm vào danh sách yêu thích
    - POST /api/customers/{user_id}/track_viewed_book/ - Theo dõi sách đã xem
    """
    
    def get_customer(self, user_id):
        """Lấy customer profile"""
        try:
            user = User.objects.get(id=user_id)
            customer = user.customer_profile
            return customer, None
        except:
            return None, "Khách hàng không tồn tại"
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Lấy profile của khách hàng"""
        customer, error = self.get_customer(pk)
        
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        """
        Thêm sách vào danh sách yêu thích
        
        POST /api/customers/{user_id}/add_to_favorites/
        Body:
        {
            "book_id": 1,
            "book_title": "Django for Beginners"
        }
        """
        
        customer, error = self.get_customer(pk)
        
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)
        
        book_id = request.data.get('book_id')
        book_title = request.data.get('book_title')
        
        if not book_id:
            return Response(
                {'error': 'Cần cung cấp book_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Kiểm tra đã yêu thích chưa
        favorite_books = customer.favorite_books
        
        if any(b['id'] == book_id for b in favorite_books):
            return Response(
                {'error': 'Sách này đã được thêm vào danh sách yêu thích'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Thêm sách
        favorite_books.append({
            'id': book_id,
            'title': book_title,
            'added_at': str(timezone.now())
        })
        
        customer.favorite_books = favorite_books
        customer.save()
        
        return Response({
            'message': 'Đã thêm vào danh sách yêu thích',
            'favorite_books': favorite_books
        })
    
    @action(detail=True, methods=['post'])
    def remove_from_favorites(self, request, pk=None):
        """Loại bỏ sách khỏi danh sách yêu thích"""
        
        customer, error = self.get_customer(pk)
        
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)
        
        book_id = request.data.get('book_id')
        
        favorite_books = [b for b in customer.favorite_books if b['id'] != book_id]
        customer.favorite_books = favorite_books
        customer.save()
        
        return Response({
            'message': 'Đã loại bỏ khỏi danh sách yêu thích',
            'favorite_books': favorite_books
        })
    
    @action(detail=True, methods=['post'])
    def track_viewed_book(self, request, pk=None):
        """Theo dõi sách đã xem"""
        
        from django.utils import timezone
        
        customer, error = self.get_customer(pk)
        
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)
        
        book_id = request.data.get('book_id')
        book_title = request.data.get('book_title')
        
        if not book_id:
            return Response(
                {'error': 'Cần cung cấp book_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        last_viewed = customer.last_viewed_books
        
        # Xóa nếu đã có
        last_viewed = [b for b in last_viewed if b['id'] != book_id]
        
        # Thêm vào trước
        last_viewed.insert(0, {
            'id': book_id,
            'title': book_title,
            'viewed_at': str(timezone.now())
        })
        
        # Giữ 20 cái mới nhất
        last_viewed = last_viewed[:20]
        
        customer.last_viewed_books = last_viewed
        customer.save()
        
        return Response({
            'message': 'Đã cập nhật sách đã xem',
            'last_viewed_books': last_viewed
        })

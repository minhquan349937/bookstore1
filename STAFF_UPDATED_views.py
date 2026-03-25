# api/views.py - STAFF SERVICE (Updated with Auth & Book Management)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import StaffUser, Staff
from .serializers import StaffUserSerializer, StaffProfileSerializer

class StaffUserViewSet(viewsets.ViewSet):
    """
    ViewSet cho Staff Authentication & Management
    
    Endpoints:
    - POST /api/staff-users/login/ - Đăng nhập
    - GET /api/staff-users/profile/ - Xem profile
    - PUT /api/staff-users/profile/ - Cập nhật profile
    - POST /api/staff-users/logout/ - Đăng xuất
    - GET /api/staff-users/list/ - Danh sách nhân viên (admin only)
    """
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Đăng nhập nhân viên
        
        POST /api/staff-users/login/
        Body:
        {
            "username": "staff_user",
            "password": "securepass"
        }
        """
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Cần cung cấp username và password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Xác thực
        user = authenticate(username=username, password=password)
        
        if not user or user.user_type != 'staff':
            return Response(
                {'error': 'Tên đăng nhập hoặc mật khẩu không đúng'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active_staff:
            return Response(
                {'error': 'Tài khoản nhân viên này đã bị vô hiệu hóa'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cập nhật last login
        user.last_logged_in = timezone.now()
        user.save()
        
        # Lấy hoặc tạo token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Đăng nhập thành công',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'department': user.department,
            }
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Lấy thông tin profile của staff"""
        
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Cần đăng nhập'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            staff = request.user.staff_profile
            profile_data = {
                'id': staff.id,
                'username': staff.user.username,
                'email': staff.user.email,
                'role': staff.user.role,
                'position': staff.position,
                'department': staff.user.department,
                'salary': staff.salary,
                'address': staff.address,
                'city': staff.city,
                'books_added': staff.books_added,
                'books_edited': staff.books_edited,
            }
            return Response(profile_data)
        except:
            return Response(
                {'error': 'Profile không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Đăng xuất"""
        
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Chưa đăng nhập'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        return Response({'message': 'Đăng xuất thành công'})
    
    @action(detail=False, methods=['get'])
    def list_staff(self, request):
        """
        Danh sách nhân viên (chỉ admin)
        
        GET /api/staff-users/list_staff/
        """
        
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Cần đăng nhập'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if request.user.role != 'admin':
            return Response(
                {'error': 'Không có quyền truy cập'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        staff_users = StaffUser.objects.filter(user_type='staff')
        
        data = []
        for user in staff_users:
            try:
                staff = user.staff_profile
                data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'position': staff.position,
                    'department': user.department,
                    'status': 'Hoạt động' if user.is_active_staff else 'Vô hiệu',
                    'hire_date': user.hire_date,
                })
            except:
                pass
        
        return Response({
            'count': len(data),
            'staff': data
        })


class StaffBookManagementViewSet(viewsets.ViewSet):
    """
    ViewSet cho quản lý sách bởi nhân viên
    
    Endpoints:
    - GET /api/staff-books/list/ - Danh sách sách (admin/manager/editor)
    - POST /api/staff-books/add/ - Thêm sách mới
    - POST /api/staff-books/{book_id}/edit/ - Chỉnh sửa sách
    - POST /api/staff-books/{book_id}/update_stock/ - Cập nhật tồn kho
    - GET /api/staff-books/report/ - Báo cáo sách
    """
    
    def check_permission(self, request):
        """Kiểm tra quyền chỉnh sửa"""
        if not request.user.is_authenticated:
            return False, Response(
                {'error': 'Cần đăng nhập'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not request.user.has_perm_to_edit_books():
            return False, Response(
                {'error': 'Không có quyền quản lý sách'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return True, None
    
    @action(detail=False, methods=['get'])
    def list_books(self, request):
        """
        Danh sách tất cả sách
        
        GET /api/staff-books/list/
        """
        
        has_perm, error = self.check_permission(request)
        if not has_perm:
            return error
        
        # Gọi Book Service để lấy danh sách sách
        import requests
        
        try:
            response = requests.get('http://localhost:8001/api/books/', timeout=5)
            if response.status_code == 200:
                books = response.json()
                return Response({
                    'message': 'Danh sách sách',
                    'total': len(books) if isinstance(books, list) else books.get('count', 0),
                    'books': books
                })
            else:
                return Response(
                    {'error': 'Không thể lấy danh sách sách'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except:
            return Response(
                {'error': 'Lỗi kết nối tới Book Service'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    @action(detail=False, methods=['post'])
    def add_book(self, request):
        """
        Thêm sách mới
        
        POST /api/staff-books/add/
        Body:
        {
            "title": "New Book",
            "author": "Author Name",
            "isbn": "978-1234567890",
            "genre": "science",
            "price": 29.99,
            "stock": 50,
            "publication_date": "2023-01-01",
            "publisher": "Publisher",
            "pages": 400
        }
        """
        
        has_perm, error = self.check_permission(request)
        if not has_perm:
            return error
        
        import requests
        
        try:
            response = requests.post(
                'http://localhost:8001/api/books/',
                json=request.data,
                timeout=5
            )
            
            if response.status_code == 201:
                # Cập nhật thống kê nhân viên
                staff = request.user.staff_profile
                staff.books_added += 1
                staff.save()
                
                return Response({
                    'message': 'Sách đã được thêm thành công',
                    'book': response.json()
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': response.json()},
                    status=response.status_code
                )
        except:
            return Response(
                {'error': 'Lỗi kết nối tới Book Service'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    @action(detail=False, methods=['post'])
    def edit_book(self, request):
        """
        Chỉnh sửa thông tin sách
        
        POST /api/staff-books/edit/
        Body:
        {
            "book_id": 1,
            "title": "Updated Title",
            "author": "Updated Author",
            "price": 39.99,
            ...
        }
        """
        
        has_perm, error = self.check_permission(request)
        if not has_perm:
            return error
        
        import requests
        
        book_id = request.data.get('book_id')
        
        if not book_id:
            return Response(
                {'error': 'Cần cung cấp book_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            response = requests.put(
                f'http://localhost:8001/api/books/{book_id}/',
                json=request.data,
                timeout=5
            )
            
            if response.status_code == 200:
                # Cập nhật thống kê nhân viên
                staff = request.user.staff_profile
                staff.books_edited += 1
                staff.save()
                
                return Response({
                    'message': 'Sách đã được cập nhật',
                    'book': response.json()
                })
            else:
                return Response(
                    {'error': response.json()},
                    status=response.status_code
                )
        except:
            return Response(
                {'error': 'Lỗi kết nối tới Book Service'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    @action(detail=False, methods=['post'])
    def update_stock(self, request):
        """
        Cập nhật tồn kho
        
        POST /api/staff-books/update_stock/
        Body:
        {
            "book_id": 1,
            "quantity": 50,
            "action": "increase" hoặc "decrease"
        }
        """
        
        has_perm, error = self.check_permission(request)
        if not has_perm:
            return error
        
        import requests
        
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')
        action = request.data.get('action', 'increase')
        
        if not book_id or not quantity:
            return Response(
                {'error': 'Cần cung cấp book_id và quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            endpoint = f'http://localhost:8001/api/books/{book_id}/{action}_stock/'
            
            response = requests.post(
                endpoint,
                json={'quantity': quantity},
                timeout=5
            )
            
            if response.status_code == 200:
                return Response({
                    'message': f'Tồn kho đã được {action} {quantity} cuốn',
                    'book': response.json()
                })
            else:
                return Response(
                    {'error': response.json()},
                    status=response.status_code
                )
        except:
            return Response(
                {'error': 'Lỗi kết nối tới Book Service'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
    
    @action(detail=False, methods=['get'])
    def report(self, request):
        """Báo cáo quản lý sách"""
        
        has_perm, error = self.check_permission(request)
        if not has_perm:
            return error
        
        import requests
        
        try:
            response = requests.get(
                'http://localhost:8001/api/books/stats/',
                timeout=5
            )
            
            if response.status_code == 200:
                stats = response.json()
                
                staff = request.user.staff_profile
                
                return Response({
                    'message': 'Báo cáo quản lý sách',
                    'book_stats': stats,
                    'your_statistics': {
                        'books_added': staff.books_added,
                        'books_edited': staff.books_edited,
                    }
                })
            else:
                return Response(
                    {'error': 'Không thể lấy thống kê'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except:
            return Response(
                {'error': 'Lỗi kết nối tới Book Service'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

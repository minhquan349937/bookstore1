# =====================================================================
# HƯỚNG DẪN CÁCH TRIỂN KHAI BOOKSTORE MICROSERVICES
# =====================================================================

## A. CHUẨN BỊ BAN ĐẦU

### Bước 1: Chạy script setup
```powershell
cd "C:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01"
.\setup_bookstore_microservices.ps1
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

---

## B. CẤU HÌNH TỪNG SERVICE

### Tất cả services làm theo các bước sau:

#### 1. Cập nhật INSTALLED_APPS trong settings.py

Thêm vào file `<service>/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'corsheaders',
    
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
    "http://localhost:8004",
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}
```

#### 2. Cập nhật urls.py

Thêm vào file `<service>/<service>/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

---

## C. TRIỂN KHAI TỪNG SERVICE

### BOOK SERVICE (Port 8001)

#### 1. Copy các file
- `BOOK_SERVICE_models.py` → `bookstore_microservices/book_service/api/models.py`
- `BOOK_SERVICE_serializers.py` → `bookstore_microservices/book_service/api/serializers.py`
- `BOOK_SERVICE_views.py` → `bookstore_microservices/book_service/api/views.py`
- `BOOK_SERVICE_urls.py` → `bookstore_microservices/book_service/api/urls.py`

#### 2. Tạo migrations và database
```bash
cd bookstore_microservices\book_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 3. Chạy server
```bash
python manage.py runserver 8001
```

---

### CUSTOMER SERVICE (Port 8002)

#### 1. Copy các file
- `CUSTOMER_SERVICE_models.py` → `bookstore_microservices/customer_service/api/models.py`
- `CUSTOMER_SERVICE_serializers.py` → `bookstore_microservices/customer_service/api/serializers.py`
- `CUSTOMER_SERVICE_views.py` → `bookstore_microservices/customer_service/api/views.py`

#### 2. Tạo urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
```

#### 3. Migrations và database
```bash
cd bookstore_microservices\customer_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8002
```

---

### STAFF SERVICE (Port 8003)

#### 1. Copy file models
- `STAFF_SERVICE_models.py` → `bookstore_microservices/staff_service/api/models.py`

#### 2. Tạo serializers.py
```python
from rest_framework import serializers
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
```

#### 3. Tạo views.py
```python
from rest_framework import viewsets
from .models import Staff
from .serializers import StaffSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
```

#### 4. Tạo urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffViewSet

router = DefaultRouter()
router.register(r'staff', StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
]
```

#### 5. Migrations
```bash
cd bookstore_microservices\staff_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8003
```

---

### ORDER SERVICE (Port 8004)

#### 1. Copy file models
- `ORDER_SERVICE_models.py` → `bookstore_microservices/order_service/api/models.py`

#### 2. Tạo serializers.py
```python
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'book_id', 'book_title', 'quantity', 'unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_number', 'order_date', 'created_at', 'updated_at']
```

#### 3. Tạo views.py
```python
from rest_framework import viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
```

#### 4. Tạo urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
```

#### 5. Migrations
```bash
cd bookstore_microservices\order_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8004
```

---

### API GATEWAY (Port 8000)

#### 1. Copy files
- `API_GATEWAY_views.py` → `bookstore_microservices/api_gateway/api/views.py`
- `API_GATEWAY_urls.py` → `bookstore_microservices/api_gateway/api_gateway/urls.py`

#### 2. Migrations
```bash
cd bookstore_microservices\api_gateway
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

---

## D. KIỂM TRA KẾT NỐI

### Mở 5 terminals khác nhau:

**Terminal 1 - Book Service:**
```bash
cd bookstore_microservices\book_service
python manage.py runserver 8001
```

**Terminal 2 - Customer Service:**
```bash
cd bookstore_microservices\customer_service
python manage.py runserver 8002
```

**Terminal 3 - Staff Service:**
```bash
cd bookstore_microservices\staff_service
python manage.py runserver 8003
```

**Terminal 4 - Order Service:**
```bash
cd bookstore_microservices\order_service
python manage.py runserver 8004
```

**Terminal 5 - API Gateway:**
```bash
cd bookstore_microservices\api_gateway
python manage.py runserver 8000
```

---

## E. TEST API

### Dùng Postman hoặc Insomnia:

1. **Tạo sách:**
   ```
   POST http://localhost:8001/api/books/
   Body: {
     "title": "Django for Beginners",
     "author": "William Vincent",
     "isbn": "978-1234567890",
     "genre": "science",
     "price": 29.99,
     "stock": 50,
     "publication_date": "2023-01-01",
     "publisher": "Packt",
     "pages": 400
   }
   ```

2. **Tạo khách hàng:**
   ```
   POST http://localhost:8002/api/customers/
   Body: {
     "first_name": "John",
     "last_name": "Doe",
     "email": "john@example.com",
     "phone": "0123456789",
     "address": "123 Main St",
     "city": "Hanoi",
     "postal_code": "10000",
     "country": "Vietnam"
   }
   ```

3. **Tạo đơn hàng (qua API Gateway):**
   ```
   POST http://localhost:8000/api/orders/create/
   Body: {
     "customer_id": 1,
     "items": [
       {"book_id": 1, "quantity": 2}
     ],
     "shipping_address": "123 Main St, Hanoi",
     "payment_method": "card"
   }
   ```

4. **Kiểm tra health:**
   ```
   GET http://localhost:8000/api/health/
   ```

---

## F. GỠ LỖI

### Services không kết nối được?
1. Kiểm tra tất cả 5 services đang chạy
2. Kiểm tra ports (8000-8004) không bị chiếm dụng
3. Check firewall settings
4. Xem logs trong terminal

### Database errors?
```bash
python manage.py makemigrations
python manage.py migrate
```

### Port already in use?
```powershell
netstat -ano | findstr :8001  # Kiểm tra port
taskkill /PID <PID> /F         # Tắt process
```

---

Chúc bạn thành công! 🎉

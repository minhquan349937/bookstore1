# =====================================================================
# HƯỚNG DẪN TỪNG BƯỚC - VISUAL GUIDE
# =====================================================================

## 📍 BẠN ĐANG Ở ĐÂU

✅ Tất cả file hướng dẫn + code mẫu đã sẵn sàng trong:
```
C:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01\
```

---

## 🎯 MỤC TIÊU

Tạo một **Bookstore Microservices** với 5 services chạy độc lập:
- Book Service (Sách)
- Customer Service (Khách hàng)
- Staff Service (Nhân viên)
- Order Service (Đơn hàng)
- API Gateway (Cổng API trung tâm)

---

## 📋 BƯỚC-BY-BƯỚC

### BƯỚC 1️⃣: SETUP (5 PHÚT)

#### 1.1. Mở PowerShell
```
Win + X → Windows PowerShell (Admin)
hoặc tìm PowerShell trong Start Menu
```

#### 1.2. Navigateto folder
```powershell
cd "C:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01"
```

#### 1.3. Chạy setup script
```powershell
.\setup_bookstore_microservices.ps1
```

⏳ Chờ 1-2 phút...

✅ Kết quả: Tạo folder `bookstore_microservices/` với 5 sub-folders

#### 1.4. Cài đặt dependencies
```powershell
pip install -r requirements.txt
```

⏳ Chờ 2-3 phút để download & cài...

✅ Kết quả: Django, DRF, CORS, requests được cài

---

### BƯỚC 2️⃣: COPY CODE (30 PHÚT)

Bạn sẽ copy code từ folder kiemtra01 vào các services

#### 2.1. BOOK SERVICE (Port 8001)

**Mở File Explorer:**
```
C:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01\
  bookstore_microservices\
    book_service\
      api\
        models.py  ← Copy BOOK_SERVICE_models.py vào đây
        serializers.py  ← Copy BOOK_SERVICE_serializers.py vào đây
        views.py  ← Copy BOOK_SERVICE_views.py vào đây
        urls.py  ← Copy BOOK_SERVICE_urls.py vào đây
```

**Cách copy:**
1. Mở VS Code
2. File → Open Folder → chọn folder kiemtra01
3. Trái: Xem các file mẫu
4. Phải: Paste vào đúng vị trí tương ứng

**Files cần copy:**
- `BOOK_SERVICE_models.py` → `book_service/api/models.py`
- `BOOK_SERVICE_serializers.py` → `book_service/api/serializers.py`
- `BOOK_SERVICE_views.py` → `book_service/api/views.py`
- `BOOK_SERVICE_urls.py` → `book_service/api/urls.py`

**Update settings:**
- Mở `book_service/book_service/settings.py`
- Thêm vào INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...tất cả cái có sẵn...,
    'rest_framework',
    'corsheaders',
    'api',
]
```

- Thêm vào MIDDLEWARE:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # ← Thêm dòng này
    ...cái khác...
]
```

**Update urls (project level):**
- Mở `book_service/book_service/urls.py`
- Thay đổi thành:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

#### 2.2. CUSTOMER SERVICE (Port 8002)

**Copy files:**
- `CUSTOMER_SERVICE_models.py` → `customer_service/api/models.py`
- `CUSTOMER_SERVICE_serializers.py` → `customer_service/api/serializers.py`
- `CUSTOMER_SERVICE_views.py` → `customer_service/api/views.py`

**Create urls.py:**
Tạo file `customer_service/api/urls.py`:
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

**Update settings & urls (giống Book Service)**

#### 2.3. STAFF SERVICE (Port 8003)

**Copy files:**
- `STAFF_SERVICE_models.py` → `staff_service/api/models.py`

**Create serializers.py:**
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

**Create views.py:**
```python
from rest_framework import viewsets
from .models import Staff
from .serializers import StaffSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
```

**Create urls.py:**
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

**Update settings & urls (giống trên)**

#### 2.4. ORDER SERVICE (Port 8004)

**Copy files:**
- `ORDER_SERVICE_models.py` → `order_service/api/models.py`

**Create serializers.py:**
```python
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'book_id', 'book_title', 'quantity', 
                 'unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_number', 'order_date', 
                           'created_at', 'updated_at']
```

**Create views.py:**
```python
from rest_framework import viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
```

**Create urls.py:**
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

**Update settings & urls (giống trên)**

#### 2.5. API GATEWAY (Port 8000)

**Copy files:**
- `API_GATEWAY_views.py` → `api_gateway/api/views.py`
- `API_GATEWAY_urls.py` → `api_gateway/api_gateway/urls.py`

**Update settings:**
- Thêm 'api' vào INSTALLED_APPS
- Thêm rest_framework, corsheaders

---

### BƯỚC 3️⃣: DATABASE (20 PHÚT)

Chạy lệnh này cho **mỗi service** (5 lần):

#### 3.1. Book Service
```bash
cd bookstore_microservices\book_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 3.2. Customer Service
```bash
cd ..\customer_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 3.3. Staff Service
```bash
cd ..\staff_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 3.4. Order Service
```bash
cd ..\order_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 3.5. API Gateway
```bash
cd ..\api_gateway
python manage.py migrate
python manage.py createsuperuser
```

---

### BƯỚC 4️⃣: CHẠY SERVICES (2 PHÚT)

**Mở 5 PowerShell/terminals khác nhau:**

#### Terminal 1 - Book Service (Port 8001)
```bash
cd bookstore_microservices\book_service
python manage.py runserver 8001
```

#### Terminal 2 - Customer Service (Port 8002)
```bash
cd bookstore_microservices\customer_service
python manage.py runserver 8002
```

#### Terminal 3 - Staff Service (Port 8003)
```bash
cd bookstore_microservices\staff_service
python manage.py runserver 8003
```

#### Terminal 4 - Order Service (Port 8004)
```bash
cd bookstore_microservices\order_service
python manage.py runserver 8004
```

#### Terminal 5 - API Gateway (Port 8000)
```bash
cd bookstore_microservices\api_gateway
python manage.py runserver 8000
```

✅ Tất cả 5 services đang chạy!

---

### BƯỚC 5️⃣: TEST (15 PHÚT)

#### 5.1. Kiểm tra connection
Mở browser và vào:
```
http://localhost:8000/api/
```

✅ Bạn sẽ thấy danh sách services và trạng thái của chúng

#### 5.2. Dùng Postman / Insomnia

**Download Postman từ:** https://www.postman.com/downloads/

**Test Create Book:**
```
POST http://localhost:8001/api/books/

Body (JSON):
{
  "title": "Django for Beginners",
  "author": "William Vincent",
  "isbn": "978-1484222249",
  "description": "Learn Django",
  "genre": "science",
  "price": 29.99,
  "stock": 50,
  "publication_date": "2023-01-15",
  "publisher": "Packt",
  "pages": 400
}
```

**Test Create Customer:**
```
POST http://localhost:8002/api/customers/

Body (JSON):
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "0912345678",
  "address": "123 Main St",
  "city": "Hanoi",
  "postal_code": "10000",
  "country": "Vietnam"
}
```

**Test Create Order (The Best Part - Orchestration):**
```
POST http://localhost:8000/api/orders/create/

Body (JSON):
{
  "customer_id": 1,
  "items": [
    {
      "book_id": 1,
      "quantity": 2
    }
  ],
  "shipping_address": "123 Main St, Hanoi",
  "payment_method": "card"
}
```

**Kết quả:** Cái này sẽ:
✅ Kiểm tra khách hàng tồn tại
✅ Kiểm tra sách tồn tại
✅ Kiểm tra tồn kho
✅ Tự động giảm tồn kho
✅ Tạo đơn hàng
✅ Cập nhật thống kê khách hàng
✅ Trả về hoàn chỉnh order data

---

## 🎉 XONG!

Bạn đã tạo thành công:
- ✅ 5 microservices
- ✅ 5 databases
- ✅ API Gateway với orchestration
- ✅ CORS enabled
- ✅ REST API với CRUD

**Chúc mừng!** 🎊

---

## 📞 NẾU GẶP LỖI?

### Lỗi: Port đang sử dụng
```powershell
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### Lỗi: Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Lỗi: Import error
- Kiểm tra mình đã copy file vào đúng folder chưa?
- Kiểm tra settings.py thêm 'api' vào INSTALLED_APPS chưa?

---

## 📚 TÀI LIỆU THAM KHẢO

- **QUICK_START.md** - Bắt đầu nhanh
- **HUONG_DAN_CHI_TIET.md** - Chi tiết từng bước
- **DU_LIEU_SAMPLE.md** - Dữ liệu mẫu
- **ARCHITECTURE.md** - Biểu đồ & schema
- **README.md** - Danh sách tất cả file

---

**Thời gian tổng cộng:** ~1-1.5 giờ ⏱️

**Chầu bạn thành công!** 🚀

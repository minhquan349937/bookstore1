# =====================================================================
# QUICK START GUIDE - BẮT ĐẦU NHANH
# =====================================================================

## 🚀 KHỞI ĐỘNG NHANH (5 PHÚT)

### Bước 1: Chạy setup script
```powershell
cd "C:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01"
.\setup_bookstore_microservices.ps1
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Copy code mẫu

**Book Service:**
```bash
cd bookstore_microservices\book_service\api
# Copy nội dung từ các file:
# - BOOK_SERVICE_models.py → models.py
# - BOOK_SERVICE_serializers.py → serializers.py  
# - BOOK_SERVICE_views.py → views.py
# - BOOK_SERVICE_urls.py → urls.py
```

**Customer Service:** (Tương tự)
**Staff Service:** (Tương tự)
**Order Service:** (Tương tự)

### Bước 4: Cấu hình urls.py mỗi project
Trong `<service>/<service>/urls.py`, thêm:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

### Bước 5: Thêm settings
Trong `<service>/<service>/settings.py`, thêm vào INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...existing...,
    'rest_framework',
    'corsheaders',
    'api',
]
```

### Bước 6: Database migrations
Chạy trong mỗi service:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Bước 7: Chạy 5 services (mở 5 terminals)

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

## 👉 TEST NGAY

### 1. Mở browser, kiểm tra API Gateway:
```
http://localhost:8000/api/
```
Kết quả: Hiển thị danh sách services

### 2. Kiểm tra health:
```
http://localhost:8000/api/health/
```
Kết quả: Hiển thị trạng thái của tất cả services

### 3. Dùng Postman tạo sách:
```
POST http://localhost:8001/api/books/
Body:
{
  "title": "Django for Beginners",
  "author": "William Vincent",
  "isbn": "978-1484222249",
  "genre": "science",
  "price": 29.99,
  "stock": 50,
  "publication_date": "2023-01-15",
  "publisher": "Packt",
  "pages": 400
}
```

### 4. Tạo khách hàng:
```
POST http://localhost:8002/api/customers/
Body:
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

### 5. Tạo đơn hàng (Orchestration):
```
POST http://localhost:8000/api/orders/create/
Body:
{
  "customer_id": 1,
  "items": [{"book_id": 1, "quantity": 2}],
  "shipping_address": "123 Main St, Hanoi",
  "payment_method": "card"
}
```

Kết quả: Tự động giảm tồn kho, tạo đơn hàng, cập nhật thống kê

---

## 📝 CẤU TRÚC TẬP TIN

```
bookstore_microservices/
├── api_gateway/                 (Port 8000 - Cổng API)
│   ├── api/
│   │   ├── views.py            (Routing, orchestration)
│   │   └── urls.py
│   └── manage.py
│
├── book_service/               (Port 8001 - Quản lý sách)
│   ├── api/
│   │   ├── models.py           (Book model)
│   │   ├── serializers.py      (BookSerializer)
│   │   ├── views.py            (BookViewSet)
│   │   └── urls.py
│   └── manage.py
│
├── customer_service/           (Port 8002 - Quản lý khách hàng)
│   ├── api/
│   │   ├── models.py           (Customer model)
│   │   ├── serializers.py      (CustomerSerializer)
│   │   ├── views.py            (CustomerViewSet)
│   │   └── urls.py
│   └── manage.py
│
├── staff_service/              (Port 8003 - Quản lý nhân viên)
│   ├── api/
│   │   ├── models.py           (Staff model)
│   │   ├── serializers.py      (StaffSerializer)
│   │   ├── views.py            (StaffViewSet)
│   │   └── urls.py
│   └── manage.py
│
└── order_service/              (Port 8004 - Quản lý đơn hàng)
    ├── api/
    │   ├── models.py           (Order, OrderItem models)
    │   ├── serializers.py      (OrderSerializer)
    │   ├── views.py            (OrderViewSet)
    │   └── urls.py
    └── manage.py
```

---

## 🔌 API ENDPOINTS

### Book Service (8001)
- `GET/POST /api/books/` - CRUD sách
- `GET /api/books/{id}/` - Chi tiết sách
- `GET /api/books/available/` - Sách còn hàng
- `POST /api/books/{id}/decrease_stock/` - Giảm tồn kho
- `POST /api/books/{id}/increase_stock/` - Tăng tồn kho

### Customer Service (8002)
- `GET/POST /api/customers/` - CRUD khách hàng
- `GET /api/customers/{id}/` - Chi tiết khách hàng
- `GET /api/customers/top_customers/` - 10 KH chi tiêu nhiều nhất
- `POST /api/customers/{id}/update_last_login/` - Cập nhật đăng nhập
- `POST /api/customers/{id}/update_total_spent/` - Cập nhật chi tiêu

### Staff Service (8003)
- `GET/POST /api/staff/` - CRUD nhân viên
- `GET /api/staff/{id}/` - Chi tiết nhân viên

### Order Service (8004)
- `GET/POST /api/orders/` - CRUD đơn hàng
- `GET /api/orders/{id}/` - Chi tiết đơn hàng

### API Gateway (8000)
- `GET /api/` - Root endpoint (đã cấu hình sẵn)
- `GET /api/health/` - Kiểm tra trạng thái services
- `POST /api/orders/create/` - Tạo đơn hàng (orchestration)

---

## 🛠️ TROUBLESHOOTING

### Port đang sử dụng?
```powershell
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Lỗi import?
```bash
pip install -r requirements.txt
```

### Database error?
```bash
python manage.py makemigrations
python manage.py migrate
```

### Module not found?
- Kiểm tra mình đã copy file models.py, serializers.py, views.py chưa?
- Kiểm tra INSTALLED_APPS đã thêm 'api' chưa?

---

## 📚 FILE THAM KHẢO

Tất cả code mẫu nằm trong folder kiemtra01:
- `BOOK_SERVICE_*.py` - Code cho Book Service
- `CUSTOMER_SERVICE_*.py` - Code cho Customer Service
- `STAFF_SERVICE_*.py` - Code cho Staff Service
- `ORDER_SERVICE_*.py` - Code cho Order Service
- `API_GATEWAY_*.py` - Code cho API Gateway
- `HUONG_DAN_CHI_TIET.md` - Hướng dẫn chi tiết
- `DU_LIEU_SAMPLE.md` - Dữ liệu mẫu để test
- `requirements.txt` - Danh sách packages cần cài

---

Bất kỳ vấn đề gì, hãy kiểm tra HUONG_DAN_CHI_TIET.md! 📖

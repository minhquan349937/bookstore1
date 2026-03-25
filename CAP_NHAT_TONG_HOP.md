# =====================================================================
# CẬP NHẬT TỔNG HỢP - DANH SÁCH CÁC FILE MỚI VÀ CẬP NHẬT
# =====================================================================

## 📋 TỌA ĐỖ - CÁC FILE ĐÃ THÊM/CẬP NHẬT

### 🆕 CÁC FILE HOÀN TOÀN MỚI (17 file)

#### CART SERVICE (PORT 8005) - SERVICE MỚI
1. **CART_SERVICE_models.py**
   - Model `Cart`: Giỏ hàng
   - Model `CartItem`: Chi tiết giỏ hàng
   → Sao chép vào `cart_service/api/models.py`

2. **CART_SERVICE_serializers.py**
   - `CartItemSerializer`
   - `CartSerializer`
   → Sao chép vào `cart_service/api/serializers.py`

3. **CART_SERVICE_views.py**
   - `CartViewSet` với endpoints: add_item, remove_item, update_quantity, clear
   → Sao chép vào `cart_service/api/views.py`

4. **CART_SERVICE_urls.py**
   - Router cho Cart
   → Sao chép vào `cart_service/api/urls.py`

#### CUSTOMER SERVICE - CẬP NHẬT VỚI AUTH
5. **CUSTOMER_UPDATED_models.py**
   - Model `User` (extends AbstractUser)
   - Model `Customer` (profile mới)
   → THAY TẮT cái cũ `customer_service/api/models.py`

6. **CUSTOMER_UPDATED_serializers.py**
   - `UserSerializer` - Đăng ký
   - `UserLoginSerializer` - Đăng nhập
   - `UserDetailSerializer` - Chi tiết user
   - `CustomerSerializer` - Customer profile
   → THAY TẮT cái cũ `customer_service/api/serializers.py`

7. **CUSTOMER_UPDATED_views.py**
   - `UserViewSet`: register, login, profile, logout, change_password
   - `CustomerViewSet`: favorites, track_viewed_books
   → THAY TẮT cái cũ `customer_service/api/views.py`

8. **CUSTOMER_UPDATED_urls.py**
   - Router cho User và Customer
   → THAY TẮT cái cũ `customer_service/api/urls.py`

#### BOOK SERVICE - CẬP NHẬT VỚI SEARCH & MANAGEMENT
9. **BOOK_SERVICE_UPDATED_views.py**
   - `BookViewSet` với endpoints mới:
     - `/search/` - Tìm kiếm nâng cao
     - `/by_genre/` - Theo thể loại
     - `/available/` - Sách còn hàng
     - `/update_price/` - Cập nhật giá
     - `/update_all_info/` - Cập nhật toàn bộ
     - `/bulk_upload/` - Upload hàng loạt
     - `/stats/` - Thống kê
   → THAY TẮT `book_service/api/views.py`

#### STAFF SERVICE - CẬP NHẬT VỚI AUTH & BOOK MANAGEMENT
10. **STAFF_UPDATED_models.py**
    - Model `StaffUser` (extends AbstractUser)
    - Model `Staff` (profile mới)
    → THAY TẮT `staff_service/api/models.py`

11. **STAFF_UPDATED_serializers.py**
    - `StaffUserSerializer`
    - `StaffProfileSerializer`
    → Sao chép vào `staff_service/api/serializers.py` (FILE MỚI)

12. **STAFF_UPDATED_views.py**
    - `StaffUserViewSet`: login, profile, logout, list_staff
    - `StaffBookManagementViewSet`: list_books, add_book, edit_book, update_stock, report
    → THAY TẮT `staff_service/api/views.py`

13. **STAFF_UPDATED_urls.py**
    - Router cho StaffUser và StaffBookManagement
    → THAY TẮT `staff_service/api/urls.py`

#### DOCUMENTATION
14. **HUONG_DAN_CHUC_NANG_MOI.md** ⭐⭐⭐
    - Hướng dẫn chi tiết tất cả chức năng mới
    - API examples đầy đủ
    - Flow cho khách hàng & nhân viên
    - Setup Cart Service

---

### 📋 TÓMLẠI CÁC CẬP NHẬT

#### Services Cần CẬP NHẬT (không phải file mới)

| Service | File Cấp NHẬT | Hành động |
|---------|---------|---------|
| **Customer Service** | models.py | THAY TẮT với CUSTOMER_UPDATED_models.py |
| | serializers.py | THAY TẮT với CUSTOMER_UPDATED_serializers.py |
| | views.py | THAY TẮT với CUSTOMER_UPDATED_views.py |
| | urls.py | THAY TẮT với CUSTOMER_UPDATED_urls.py |
| | settings.py | Thêm `rest_framework.authtoken` vào INSTALLED_APPS |
| **Book Service** | views.py | THAY TẮT với BOOK_SERVICE_UPDATED_views.py |
| **Staff Service** | models.py | THAY TẮT với STAFF_UPDATED_models.py |
| | serializers.py | TẠO MỚI file này, copy STAFF_UPDATED_serializers.py |
| | views.py | THAY TẮT với STAFF_UPDATED_views.py |
| | urls.py | THAY TẮT với STAFF_UPDATED_urls.py |
| | settings.py | Thêm `rest_framework.authtoken` vào INSTALLED_APPS |
| **API Gateway** | Không thay đổi | (Giữ nguyên) |
| **Order Service** | Không thay đổi | (Giữ nguyên) |
| **Cart Service (MỚI)** | - | Tạo service mới (xem hướng dẫn) |

---

## 🚀 BƯỚC TRIỂN KHAI

### BƯỚC 1: Cập nhật Customer Service

**1.1. Cập nhật models.py**
```bash
# Thay toàn bộ nội dung cũ bằng CUSTOMER_UPDATED_models.py
```

**1.2. Cập nhật serializers.py**
```bash
# Thay toàn bộ nội dung cũ bằng CUSTOMER_UPDATED_serializers.py
```

**1.3. Cập nhật views.py**
```bash
# Thay toàn bộ nội dung cũ bằng CUSTOMER_UPDATED_views.py
```

**1.4. Cập nhật urls.py**
```bash
# Thay toàn bộ nội dung cũ bằng CUSTOMER_UPDATED_urls.py
```

**1.5. Cập nhật settings.py**
```python
# Thêm vào INSTALLED_APPS:
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',  # ← THÊM DÒNG NÀY
    'corsheaders',
    'api',
]

# Thêm cấu hình REST Framework:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# Thêm CORS:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
    "http://localhost:8004",
    "http://localhost:8005",  # Cart Service mới
]
```

**1.6. Database migrations**
```bash
cd customer_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

### BƯỚC 2: Cập nhật Book Service

**2.1. Cập nhật views.py**
```bash
# Sao chép  toàn bộ BOOK_SERVICE_UPDATED_views.py thay vào views.py cũ
# Chú ý: Thêm import "from django.db import models" nếu thiếu
```

**2.2. Không cần migrations** (chỉ thêm endpoints)

**2.3. Test**
```bash
python manage.py runserver 8001
# Truy cập: http://localhost:8001/api/books/search/?q=django
```

---

### BƯỚC 3: Cập nhật Staff Service

**3.1. Cập nhật models.py**
```bash
# Thay toàn bộ nội dung cũ bằng STAFF_UPDATED_models.py
```

**3.2. Tạo FILE MỚI: serializers.py**
```bash
# Tạo file api/serializers.py với nội dung STAFF_UPDATED_serializers.py
```

**3.3. Cập nhật views.py**
```bash
# Thay toàn bộ nội dung cũ bằng STAFF_UPDATED_views.py
```

**3.4. Cập nhật urls.py**
```bash
# Thay toàn bộ nội dung cũ bằng STAFF_UPDATED_urls.py
```

**3.5. Cập nhật settings.py**
```python
# Tương tự Customer Service:
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',  # ← THÊM DÒNG NÀY
    'corsheaders',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    ...
}

CORS_ALLOWED_ORIGINS = [
    ...
    "http://localhost:8005",  # Cart Service
]
```

**3.6. Database migrations**
```bash
cd staff_service
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Tạo staff user với role=admin
# Hoặc tạo bằng Django admin
```

---

### BƯỚC 4: Tạo Cart Service (SERVICE MỚI)

**4.1. Tạo service**
```bash
cd bookstore_microservices
django-admin startproject cart_service cart_service
cd cart_service
python manage.py startapp api
```

**4.2. Copy code**
Sao chép vào từng file:
- `CART_SERVICE_models.py` → `api/models.py`
- `CART_SERVICE_serializers.py` → `api/serializers.py`
- `CART_SERVICE_views.py` → `api/views.py`
- `CART_SERVICE_urls.py` → `api/urls.py`

**4.3. Cập nhật settings.py**
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'api',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
    "http://localhost:8004",
    "http://localhost:8005",
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}
```

**4.4. Cập nhật main urls.py**
```python
# cart_service/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

**4.5. Database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8005
```

---

### BƯỚC 5: Chạy Toàn Bộ Services (6 services)

Mở 6 terminals khác nhau:

```bash
# Terminal 1
cd bookstore_microservices\book_service
python manage.py runserver 8001

# Terminal 2
cd bookstore_microservices\customer_service
python manage.py runserver 8002

# Terminal 3
cd bookstore_microservices\staff_service
python manage.py runserver 8003

# Terminal 4
cd bookstore_microservices\order_service
python manage.py runserver 8004

# Terminal 5
cd bookstore_microservices\cart_service
python manage.py runserver 8005

# Terminal 6
cd bookstore_microservices\api_gateway
python manage.py runserver 8000
```

---

## ✨ CHỨC NĂNG MỚI

### 👥 KHÁCH HÀNG
✅ Đăng ký & đăng nhập (Token auth)  
✅ Xem profile & cập nhật thông tin  
✅ Tìm kiếm & filter sách  
✅ Quản lý giỏ hàng đầy đủ  
✅ Danh sách yêu thích  
✅ Theo dõi sách đã xem  

### 👔 NHÂN VIÊN
✅ Đăng nhập Admin/Staff (Token auth)  
✅ Xem danh sách sách  
✅ Thêm sách mới  
✅ Chỉnh sửa thông tin sách  
✅ Cập nhật tồn kho  
✅ Xem báo cáo thống kê  
✅ Quản lý quyền (role-based)  

---

## 📞 QUICK TEST

### Đăng ký khách hàng:
```bash
POST http://localhost:8002/api/users/register/
Body: {...}
→ Nhận token
```

### Đăng nhập nhân viên:
```bash
POST http://localhost:8003/api/staff-users/login/
Body: {...}
→ Nhận token
```

### Thêm vào giỏ:
```bash
POST http://localhost:8005/api/carts/{customer_id}/add_item/
Body: {...}
```

### Xem giỏ:
```bash
GET http://localhost:8005/api/carts/{customer_id}/
```

---

## 📊 SUMMARY

| Service | Port | Status | Chức năng |
|---------|------|--------|---------|
| API Gateway | 8000 | ✅ Giữ nguyên | Routing & orchestration |
| Book Service | 8001 | ✅ Cập nhật | Search, filter, stats |
| Customer Service | 8002 | ✅ Cập nhật | Auth, profile, favorites |
| Staff Service | 8003 | ✅ Cập nhật | Auth, book management |
| Order Service | 8004 | ✅ Giữ nguyên | Tạo/quản lý đơn |
| **Cart Service** | **8005** | **✅ MỚI** | **Quản lý giỏ hàng** |

**Tổng:** 6 services, 27 file code, 600+ lines per service

---

Bây giờ bạn đã có một **Bookstore Management System** hoàn chỉnh! 🎉

Hãy đọc **HUONG_DAN_CHUC_NANG_MOI.md** để xem chi tiết từng endpoint! 📖

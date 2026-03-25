# ==============================================================================
# HƯỚNG DẪN CẤU HÌNH BOOKSTORE MICROSERVICES
# ==============================================================================

## 1. CÀI ĐẶT BAN ĐẦU

### Bước 1: Chạy script setup
```powershell
.\setup_bookstore_microservices.ps1
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## 2. CẤU TRÚC MICROSERVICES

### 2.1 BOOK SERVICE (Quản lý sách)
**URL Base:** http://localhost:8001

**Endpoints:**
- GET /api/books/ - Lấy danh sách sách
- POST /api/books/ - Tạo sách mới
- GET /api/books/{id}/ - Lấy chi tiết sách
- PUT /api/books/{id}/ - Cập nhật sách
- DELETE /api/books/{id}/ - Xóa sách

### 2.2 CUSTOMER SERVICE (Quản lý khách hàng)
**URL Base:** http://localhost:8002

**Endpoints:**
- GET /api/customers/ - Danh sách khách hàng
- POST /api/customers/ - Tạo khách hàng mới
- GET /api/customers/{id}/ - Chi tiết khách hàng
- PUT /api/customers/{id}/ - Cập nhật khách hàng
- DELETE /api/customers/{id}/ - Xóa khách hàng

### 2.3 STAFF SERVICE (Quản lý nhân viên)
**URL Base:** http://localhost:8003

**Endpoints:**
- GET /api/staff/ - Danh sách nhân viên
- POST /api/staff/ - Tạo nhân viên mới
- GET /api/staff/{id}/ - Chi tiết nhân viên
- PUT /api/staff/{id}/ - Cập nhật nhân viên

### 2.4 ORDER SERVICE (Quản lý đơn hàng)
**URL Base:** http://localhost:8004

**Endpoints:**
- GET /api/orders/ - Danh sách đơn hàng
- POST /api/orders/ - Tạo đơn hàng mới
- GET /api/orders/{id}/ - Chi tiết đơn hàng
- PUT /api/orders/{id}/ - Cập nhật đơn hàng

### 2.5 API GATEWAY (Cổng API trung tâm)
**URL Base:** http://localhost:8000

**Chức năng:**
- Định tuyến requests đến các services tương ứng
- Xác thực người dùng
- Kiểm soát truy cập (Access Control)

## 3. CHẠY TỪNG SERVICE

### Terminal 1 - Book Service
```bash
cd bookstore_microservices\book_service
python manage.py runserver 8001
```

### Terminal 2 - Customer Service
```bash
cd bookstore_microservices\customer_service
python manage.py runserver 8002
```

### Terminal 3 - Staff Service
```bash
cd bookstore_microservices\staff_service
python manage.py runserver 8003
```

### Terminal 4 - Order Service
```bash
cd bookstore_microservices\order_service
python manage.py runserver 8004
```

### Terminal 5 - API Gateway
```bash
cd bookstore_microservices\api_gateway
python manage.py runserver 8000
```

## 4. KIỂM TRA KẾT NỐI

Mở browser và kiểm tra:
- http://localhost:8000/api/ - API Gateway
- http://localhost:8001/api/ - Book Service
- http://localhost:8002/api/ - Customer Service
- http://localhost:8003/api/ - Staff Service
- http://localhost:8004/api/ - Order Service

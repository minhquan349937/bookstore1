# =====================================================================
# DANH SÁCH TẤT CẢ FILE VÀ HƯỚNG DẪN SỬ DỤNG
# =====================================================================

## 📂 FOLDER HIỆN TẠI: kiemtra01

Các file dưới đây đã được tạo sẵn:

---

## 🔧 SETUP & CẤU HÌNH

### 1. setup_bookstore_microservices.ps1
**Chức năng:** Tự động tạo cấu trúc thư mục 5 services
**Chạy lệnh:**
```powershell
.\setup_bookstore_microservices.ps1
```
**Kết quả:** Tạo folder `bookstore_microservices/` với 5 projects Django

### 2. requirements.txt
**Chức năng:** Danh sách packages Python cần cài đặt
**Chạy lệnh:**
```bash
pip install -r requirements.txt
```
**Cài đặt:** Django, DRF, CORS, requests, v.v.

---

## 📖 HƯỚNG DẪN (MARKDOWN)

### 3. QUICK_START.md ⭐⭐⭐
**ĐỌC TRƯỚC TIÊN!**
- Bước khởi động nhanh (5 phút)
- Cấu trúc tập tin
- API endpoints
- Troubleshooting

### 4. HUONG_DAN_CHI_TIET.md
**Chi tiết từng bước:**
- Copy code cho mỗi service
- Cấu hình settings.py
- Database migrations
- Chạy từng service
- Test API
- Gỡ lỗi

### 5. HUONG_DAN_SETUP.md
**Tổng quát:**
- Cấu trúc microservices
- Endpoints của mỗi service
- Cách chạy từng service

### 6. DU_LIEU_SAMPLE.md
**Data mẫu để test:**
- JSON mẫu cho 5 sách (Books)
- JSON mẫu cho 3 khách hàng (Customers)
- JSON mẫu cho 3 nhân viên (Staff)
- JSON mẫu cho đơn hàng (Orders)
- Cách kiểm tra dữ liệu
- Filter & search examples

---

## 💾 CODE MẪU - BOOK SERVICE (Port 8001)

### 7. BOOK_SERVICE_models.py
**Copy vào:** `bookstore_microservices/book_service/api/models.py`
- Model `Book` với các fields: title, author, isbn, price, stock, v.v.

### 8. BOOK_SERVICE_serializers.py
**Copy vào:** `bookstore_microservices/book_service/api/serializers.py`
- Serializer cho `Book` model
- Validation cho giá tiền và tồn kho

### 9. BOOK_SERVICE_views.py
**Copy vào:** `bookstore_microservices/book_service/api/views.py`
- ViewSet cho Book với endpoints CRUD
- Action: available, decrease_stock, increase_stock

### 10. BOOK_SERVICE_urls.py
**Copy vào:** `bookstore_microservices/book_service/api/urls.py`
- Router Django REST Framework cho Book

### 11. BOOK_SERVICE_settings.txt
**Hướng dẫn:** Thêm vào `bookstore_microservices/book_service/book_service/settings.py`
- INSTALLED_APPS
- MIDDLEWARE
- CORS settings
- REST_FRAMEWORK config

---

## 💾 CODE MẪU - CUSTOMER SERVICE (Port 8002)

### 12. CUSTOMER_SERVICE_models.py
**Copy vào:** `bookstore_microservices/customer_service/api/models.py`
- Model `Customer` với fields: name, email, phone, address, v.v.

### 13. CUSTOMER_SERVICE_serializers.py
**Copy vào:** `bookstore_microservices/customer_service/api/serializers.py`
- Serializer cho `Customer` model
- Validation cho email và số điện thoại

### 14. CUSTOMER_SERVICE_views.py
**Copy vào:** `bookstore_microservices/customer_service/api/views.py`
- ViewSet cho Customer
- Action: top_customers, update_last_login, update_total_spent

---

## 💾 CODE MẪU - STAFF SERVICE (Port 8003)

### 15. STAFF_SERVICE_models.py
**Copy vào:** `bookstore_microservices/staff_service/api/models.py`
- Model `Staff` với fields: name, email, position, salary, v.v.

---

## 💾 CODE MẪU - ORDER SERVICE (Port 8004)

### 16. ORDER_SERVICE_models.py
**Copy vào:** `bookstore_microservices/order_service/api/models.py`
- Model `Order`: Đơn hàng chính
- Model `OrderItem`: Chi tiết mặt hàng trong đơn hàng

---

## 💾 CODE MẪUAPI GATEWAY (Port 8000)

### 17. API_GATEWAY_views.py
**Copy vào:** `bookstore_microservices/api_gateway/api/views.py`
- Function `api_root()` - Hiển thị danh sách services
- Function `check_services_status()` - Kiểm tra trạng thái
- Function `health_check()` - Health check endpoint
- Function `create_order()` - **Orchestration**: Tạo đơn hàng từ multiple services

### 18. API_GATEWAY_urls.py
**Copy vào:** `bookstore_microservices/api_gateway/api_gateway/urls.py`
- URLs cho API Gateway

---

## 🚀 QUY TRÌNH TRIỂN KHAI

### Bước 1: Chạy setup (1 lần)
```powershell
.\setup_bookstore_microservices.ps1
pip install -r requirements.txt
```

### Bước 2: Copy code (5 lần)
- Mỗi service: Copy models.py, serializers.py, views.py, urls.py

### Bước 3: Cấu hình (5 lần)
- Mỗi service:
  - Add INSTALLED_APPS trong settings.py
  - Add CORS middleware
  - Update urls.py trong project folder

### Bước 4: Database (5 lần)
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Bước 5: Chạy services (5 terminals)
```bash
python manage.py runserver 8001  # Book
python manage.py runserver 8002  # Customer
python manage.py runserver 8003  # Staff
python manage.py runserver 8004  # Order
python manage.py runserver 8000  # Gateway
```

### Bước 6: Test (Postman/Insomnia)
- Dùng dữ liệu mẫu từ DU_LIEU_SAMPLE.md

---

## 📋 CHECKLIST

### Preparation:
- [ ] Scale setup script
- [ ] Install requirements.txt
- [ ] Đọc QUICK_START.md

### Book Service:
- [ ] Copy models.py
- [ ] Copy serializers.py
- [ ] Copy views.py
- [ ] Copy urls.py
- [ ] Update settings.py
- [ ] Update project urls.py
- [ ] makemigrations & migrate
- [ ] createsuperuser
- [ ] Test runserver 8001

### Customer Service:
- [ ] (Tương tự Book Service)
- [ ] Test runserver 8002

### Staff Service:
- [ ] (Tương tự Book Service)
- [ ] Test runserver 8003

### Order Service:
- [ ] Copy models.py (Order + OrderItem)
- [ ] Create serializers.py (chưa có mẫu, xem HUONG_DAN_CHI_TIET.md)
- [ ] Create views.py (chưa có mẫu, xem HUONG_DAN_CHI_TIET.md)
- [ ] Create urls.py (chưa có mẫu, xem HUONG_DAN_CHI_TIET.md)
- [ ] Update settings.py
- [ ] Update project urls.py
- [ ] makemigrations & migrate
- [ ] createsuperuser
- [ ] Test runserver 8004

### API Gateway:
- [ ] Copy views.py
- [ ] Copy urls.py
- [ ] Update settings.py
- [ ] migrate
- [ ] createsuperuser
- [ ] Test runserver 8000

### Testing:
- [ ] Test /api/ endpoint
- [ ] Test /api/health/ endpoint
- [ ] Create book (Postman)
- [ ] Create customer (Postman)
- [ ] Create order via gateway (Postman)
- [ ] Verify orchestration works

---

## 🎯 KEY FEATURES

1. **REST API** - Mỗi service cung cấp CRUD endpoints
2. **Microservices** - 5 services độc lập chạy trên ports khác nhau
3. **API Gateway** - Định tuyến requests và orchestration
4. **CORS** - Cho phép cross-origin requests
5. **Database** - SQLite cho mỗi service (separate databases)
6. **Serializers** - Validation và transformation dữ liệu
7. **ViewSets** - Tự động generate CRUD endpoints
8. **Orchestration** - API Gateway gọi multiple services để tạo order

---

## 📞 KHI CẦN GIÚP

1. Đọc QUICK_START.md
2. Kiểm tra HUONG_DAN_CHI_TIET.md
3. Xem DU_LIEU_SAMPLE.md để test
4. Check terminal logs

---

Chúc bạn thành công! 🎉

---

**Ngày tạo:** 25/03/2026
**Version:** 1.0
**Status:** Ready to Use ✅

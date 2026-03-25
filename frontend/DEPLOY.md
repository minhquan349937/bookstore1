# 🚀 Hướng Dẫn Deploy Frontend BookStore

## ✅ Yêu Cầu

- Python 3.7+ hoặc Node.js 12+
- Web browser hiện đại (Chrome, Firefox, Edge)
- Các microservices đang chạy (Customer, Book, Cart services)

---

## 🏃 Cách 1: Chạy Với Python (Khuyên dùng)

### Bước 1: Mở Terminal/PowerShell
```bash
cd c:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01\frontend
```

### Bước 2: Chạy HTTP Server
```bash
python -m http.server 8080
```

### Bước 3: Truy cập Frontend
```
http://localhost:8080/index.html
```

---

## 🏃 Cách 2: Chạy Với Live Server (VS Code)

### Bước 1: Cài đặt extension
1. Mở VS Code
2. Vào **Extensions** (Ctrl+Shift+X)
3. Tìm "Live Server"
4. Cài đặt bởi Ritwick Dey

### Bước 2: Chạy
1. Right-click vào `index.html`
2. Chọn "Open with Live Server"
3. Trình duyệt sẽ tự mở

---

## 🏃 Cách 3: Chạy Với Node.js

### Bước 1: Cài đặt http-server
```bash
npm install -g http-server
```

### Bước 2: Chạy
```bash
cd c:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01\frontend
http-server -p 8080
```

---

## 🏃 Cách 4: Deploy Với Nginx (Production)

### Bước 1: Cài đặt Nginx
```bash
# Windows: Tải từ https://nginx.org/en/download.html
# Hoặc dùng Chocolatey:
choco install nginx
```

### Bước 2: Cấu hình Nginx (`nginx.conf`)
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root C:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01\frontend;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests
    location /api/ {
        proxy_pass http://localhost:8000/api/;
    }
}
```

### Bước 3: Chạy Nginx
```bash
nginx
```

---

## 🏃 Cách 5: Deploy Với Docker

### Bước 1: Tạo Dockerfile
```dockerfile
FROM nginx:latest
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Bước 2: Build Image
```bash
docker build -t bookstore-frontend .
```

### Bước 3: Chạy Container
```bash
docker run -p 8080:80 bookstore-frontend
```

---

## 🌐 Kiểm Tra Kết Nối API

Trước khi dùng frontend, đảm bảo các services đang chạy:

```bash
# 1. Customer Service
cd bookstore_microservices/customer_service
python manage.py runserver 8002

# 2. Book Service
cd bookstore_microservices/book_service
python manage.py runserver 8001

# 3. Cart Service
cd bookstore_microservices/cart_service
python manage.py runserver 8005

# 4. API Gateway
cd bookstore_microservices/api_gateway
python manage.py runserver 8000
```

---

## 🧪 Test API Endpoints

### Đăng ký
```bash
curl -X POST http://localhost:8002/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "phone": "0123456789",
    "address": "123 Main St"
  }'
```

### Đăng nhập
```bash
curl -X POST http://localhost:8002/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Lấy danh sách sách
```bash
curl http://localhost:8001/api/books/
```

### Tìm kiếm sách
```bash
curl "http://localhost:8001/api/books/search/?q=django&sort=price_asc"
```

---

## 📊 Kiểm Tra Browser DevTools

1. Mở **F12** (Developer Console)
2. **Network** tab: Kiểm tra API requests
3. **Application** tab → **Local Storage**: Kiểm tra token
4. **Console** tab: Xem error messages

---

## 🔧 Troubleshooting

### Lỗi: "CORS Error"
**Giải pháp:** Thêm CORS headers vào Django settings.py
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

### Lỗi: "API not found"
**Giải pháp:** Kiểm tra services đang chạy trên cổng 8000-8005

### Lỗi: "Token expired"
**Giải pháp:** Xóa localStorage và đăng nhập lại
```javascript
// Developer Console
localStorage.clear();
location.reload();
```

---

## 📋 Checklist Deploy

- [ ] Python/Node.js đã cài đặt
- [ ] Tất cả microservices đang chạy
- [ ] CORS đã bật
- [ ] Frontend có thể truy cập trên port 8080
- [ ] Có thể đăng ký tài khoản
- [ ] Có thể đăng nhập
- [ ] Có thể xem danh sách sách
- [ ] Có thể tìm kiếm sách
- [ ] Có thể thêm vào giỏ hàng
- [ ] Có thể thanh toán

---

**Ready to deploy! 🚀**

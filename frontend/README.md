# 📚 BookStore Frontend - Hướng Dẫn Sử Dụng

## 🎯 Tổng Quan

Đây là giao diện khách hàng cho hệ thống BookStore Microservices, được xây dựng bằng:
- **HTML5** - Markup từ chuẩn
- **Bootstrap 5** - Framework CSS responsive
- **Vanilla JavaScript** - Không sử dụng framework JS
- **Fetch API** - Gọi API từ các microservices

## 📁 Cấu Trúc Thư Mục

```
frontend/
├── index.html           # Trang chủ - danh sách sách
├── login.html          # Trang đăng nhập
├── register.html       # Trang đăng ký
├── detail.html         # Trang chi tiết sách
├── cart.html           # Trang giỏ hàng
├── css/
│   └── common.css      # CSS chung cho tất cả trang
└── js/
    └── common.js       # JavaScript chung (API, Auth)
```

## 🔐 Các Trang Chính

### 1. **Login & Register** (`login.html` / `register.html`)
- Form đăng nhập/đăng ký
- Gọi API: `/api/users/login/` và `/api/users/register/`
- Lưu token vào `localStorage` (key: `authToken`)
- Lưu customer ID (key: `customerId`)
- Lưu thông tin user (key: `currentUser`)

**Endpoint:**
```
POST /api/users/register/
{
    "username": "string",
    "email": "string",
    "password": "string",
    "phone": "string",
    "address": "string"
}

POST /api/users/login/
{
    "username": "string",
    "password": "string"
}
Response:
{
    "token": "string",
    "customer_id": number,
    "username": "string",
    "email": "string"
}
```

### 2. **Trang Chủ** (`index.html`)
- Hiển thị danh sách sách (12 sách/trang)
- Thanh tìm kiếm và lọc theo:
  - `sort`: `newest`, `price_asc`, `price_desc`, `popular`
- Pagination
- Click vào sách chuyển sang trang chi tiết

**Endpoint:**
```
GET /api/books/?page=1&limit=12
GET /api/books/search/?q=query&sort=newest&page=1
Response:
{
    "results": [
        {
            "id": number,
            "title": "string",
            "author": "string",
            "price": number,
            "stock": number,
            "cover_image": "url"
        }
    ],
    "total_pages": number
}
```

### 3. **Trang Chi Tiết** (`detail.html`)
- Hiển thị thông tin đầy đủ 1 cuốn sách:
  - Tiêu đề, tác giả, giá, mô tả
  - Nhà xuất bản, thể loại, năm xuất bản, số trang, ISBN
  - Số lượng tồn kho
- Selector tăng/giảm số lượng
- Nút "Thêm vào giỏ hàng"

**Endpoint:**
```
GET /api/books/{id}/
Response:
{
    "id": number,
    "title": "string",
    "author": "string",
    "price": number,
    "stock": number,
    "publisher": "string",
    "genre": "string",
    "year": number,
    "pages": number,
    "isbn": "string",
    "description": "string",
    "cover_image": "url"
}
```

### 4. **Trang Giỏ Hàng** (`cart.html`)
- Bảng danh sách sản phẩm trong giỏ
- Cột: Sách, Giá, Số lượng, Tổng tiền, Hành động
- Tóm tắt đơn hàng (tiền hàng, phí vận chuyển, tổng cộng)
- Nút:
  - 🗑️ Xóa sách
  - 🗑️ Xóa tất cả
  - ✓ Thanh toán

**Endpoint:**
```
POST /api/carts/{customer_id}/add_item/
{
    "book_id": number,
    "quantity": number
}

GET /api/carts/{customer_id}/
Response:
{
    "id": number,
    "customer_id": number,
    "total_items": number,
    "total_price": number,
    "items": [
        {
            "id": number,
            "book_id": number,
            "book_title": "string",
            "book_author": "string",
            "book_price": number,
            "quantity": number,
            "subtotal": number
        }
    ]
}

POST /api/carts/{customer_id}/remove_item/
{
    "book_id": number
}

POST /api/carts/{customer_id}/update_quantity/
{
    "book_id": number,
    "quantity": number
}

POST /api/carts/{customer_id}/clear/
```

## 🔌 API Configuration

URL cơ sở được định nghĩa trong `js/common.js`:

```javascript
const API_BASE = 'http://localhost:8000/api';
const CUSTOMER_API = 'http://localhost:8002/api';  // Customer Service
// Book Service: http://localhost:8001/api
// Cart Service: http://localhost:8005/api
```

## 🔐 Authentication

### Token Management (AuthManager)
```javascript
AuthManager.getToken()           // Lấy token
AuthManager.setToken(token)      // Lưu token
AuthManager.removeToken()        // Xóa token
AuthManager.isLoggedIn()         // Kiểm tra đã đăng nhập
AuthManager.logout()             // Đăng xuất
```

### Tự động thêm Token vào Request
```javascript
// Header sẽ tự động thêm:
Authorization: Token {token}
```

## 🎨 CSS Classes

### Thường dùng:
- `.btn-primary` - Nút xanh (Primary)
- `.btn-success` - Nút xanh lá (Success)
- `.btn-danger` - Nút đỏ (Danger)
- `.btn-outline-*` - Nút viền
- `.form-control` - Input
- `.form-label` - Label
- `.spinner` - Loading spinner

## 🚀 Chạy Frontend

### Với Python (HTTP Server)
```bash
cd frontend
python -m http.server 8080
```
Truy cập: `http://localhost:8080/index.html`

### Với Live Server (VS Code)
- Cài đặt extension "Live Server"
- Right-click vào `index.html` → "Open with Live Server"

### Với Node.js (http-server)
```bash
npm install -g http-server
cd frontend
http-server
```

## 🔄 Luồng Sử Dụng

1. **Đăng ký / Đăng nhập**
   - Truy cập `/register.html` hoặc `/login.html`
   - Token được lưu tự động

2. **Duyệt sách**
   - Truy cập `/index.html`
   - Tìm kiếm, lọc, phân trang
   - Click sách để xem chi tiết

3. **Xem chi tiết**
   - Truy cập `/detail.html?id={bookId}`
   - Chọn số lượng
   - Click "Thêm vào giỏ hàng"

4. **Quản lý giỏ hàng**
   - Truy cập `/cart.html`
   - Thay đổi số lượng hoặc xóa sBooks
   - Click "Thanh Toán"

## ⚠️ Lưu ý Quan Trọng

1. **CORS**: Các API endpoints phải hỗ trợ CORS từ origin `http://localhost:8080`
2. **Token**: Được lưu trong `localStorage`, mất đăng nhập khi xóa cache
3. **Customer ID**: Được lưu cùng token, dùng cho cart operations
4. **Responsive**: Toàn bộ giao diện đã responsive cho mobile/tablet

## 🛠️ Debug

Mở Developer Console (F12) để xem:
- Network requests
- Local Storage (Application tab)
- Console errors

## 📦 Dependencies

- Bootstrap 5.3.0 (CDN)
- Font Awesome (tuỳ chọn)
- Không cần cài đặt npm packages, toàn bộ sử dụng CDN

---

**Version:** 1.0  
**Last Updated:** 2024  
**Author:** BookStore Dev Team

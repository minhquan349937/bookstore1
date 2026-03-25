# =====================================================================
# HƯỚNG DẪN CHỨC NĂNG MỚI - CUSTOMER & STAFF
# =====================================================================

## 📌 TÓM TẮT CÁC CHỨC NĂNG MỚI

### 👥 KHÁCH HÀNG (Customer Service)

#### 1️⃣ ĐĂNG KÝ & ĐĂNG NHẬP

**Đăng ký tài khoản:**
```
POST http://localhost:8002/api/users/register/

Body:
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "0912345678",
    "address": "123 Main St",
    "city": "Hanoi"
}

Response:
{
    "message": "Đăng ký thành công",
    "user": {...},
    "token": "abc123def456..."  ← Sử dụng token này trong header Authorization
}
```

**Đăng nhập:**
```
POST http://localhost:8002/api/users/login/

Body:
{
    "username": "john_doe",
    "password": "SecurePass123"
}

Response:
{
    "message": "Đăng nhập thành công",
    "token": "abc123def456...",
    "user": {...}
}
```

**Cách sử dụng token trong requests:**
```
Header: Authorization: Token abc123def456...
```

#### 2️⃣ XEM DANH SÁCH SÁCH

**Lấy danh sách sách (có tìm kiếm & filter):**
```
GET http://localhost:8001/api/books/
    ?genre=science
    &search=django
    &min_price=20
    &max_price=50
    &in_stock_only=true
    &ordering=-price

Response: Danh sách sách với phân trang
{
    "count": 15,
    "next": "...",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Django for Beginners",
            "author": "William Vincent",
            "price": 29.99,
            "stock": 50,
            ...
        }
    ]
}
```

#### 3️⃣ TÌM KIẾM SÁCH

**Tìm kiếm nâng cao:**
```
GET http://localhost:8001/api/books/search/
    ?q=django
    &sort=price_asc

Tham số sort:
- price_asc: Giá từ thấp đến cao
- price_desc: Giá từ cao đến thấp
- newest: Mới nhất
- popular: Phổ biến nhất

Response:
{
    "count": 5,
    "results": [...]
}
```

**Tìm theo thể loại:**
```
GET http://localhost:8001/api/books/by_genre/?genre=science

Response:
{
    "genre": "science",
    "count": 12,
    "results": [...]
}
```

#### 4️⃣ QUẢN LÝ GIỎ HÀNG

**Tạo giỏ hàng (tự động):**
```
Khi thêm sản phẩm đầu tiên, giỏ hàng sẽ được tạo tự động
```

**Thêm vào giỏ hàng:**
```
POST http://localhost:8005/api/carts/{customer_id}/add_item/

Body:
{
    "book_id": 1,
    "book_title": "Django for Beginners",
    "book_author": "William Vincent",
    "book_price": 29.99,
    "quantity": 2
}

Response:
{
    "id": 1,
    "customer_id": 1,
    "items": [
        {
            "id": 1,
            "book_id": 1,
            "book_title": "Django for Beginners",
            "quantity": 2,
            "subtotal": 59.98
        }
    ],
    "total_items": 2,
    "total_price": 59.98
}
```

**Xem giỏ hàng:**
```
GET http://localhost:8005/api/carts/{customer_id}/

Response: Toàn bộ chi tiết giỏ hàng
{
    "id": 1,
    "customer_id": 1,
    "items": [...],
    "total_items": 2,
    "total_price": 59.98,
    "updated_at": "2026-03-25T..."
}
```

**Cập nhật số lượng:**
```
POST http://localhost:8005/api/carts/{customer_id}/update_quantity/

Body:
{
    "book_id": 1,
    "quantity": 3
}

Response: Giỏ hàng cập nhật
```

**Xóa sách khỏi giỏ:**
```
POST http://localhost:8005/api/carts/{customer_id}/remove_item/

Body:
{
    "book_id": 1
}

Response: Giỏ hàng cập nhật (không có sách này nữa)
```

**Xóa toàn bộ giỏ:**
```
POST http://localhost:8005/api/carts/{customer_id}/clear/

Response: Giỏ hàng trống (total_items: 0, total_price: 0)
```

#### 5️⃣ DANH SÁCH YÊU THÍCH & SÁCH ĐÃ XEM

**Thêm vào danh sách yêu thích:**
```
POST http://localhost:8002/api/customers/{user_id}/add_to_favorites/

Body:
{
    "book_id": 1,
    "book_title": "Django for Beginners"
}

Response:
{
    "message": "Đã thêm vào danh sách yêu thích",
    "favorite_books": [
        {
            "id": 1,
            "title": "Django for Beginners",
            "added_at": "2026-03-25T..."
        }
    ]
}
```

**Loại bỏ khỏi danh sách yêu thích:**
```
POST http://localhost:8002/api/customers/{user_id}/remove_from_favorites/

Body:
{
    "book_id": 1
}
```

**Theo dõi sách đã xem:**
```
POST http://localhost:8002/api/customers/{user_id}/track_viewed_book/

Body:
{
    "book_id": 1,
    "book_title": "Django for Beginners"
}

Response:
{
    "message": "Đã cập nhật sách đã xem",
    "last_viewed_books": [
        {
            "id": 1,
            "title": "Django for Beginners",
            "viewed_at": "2026-03-25T..."
        },
        ...
    ]
}

Lưu ý: Giữ 20 sách xem gần đây
```

---

### 👔 NHÂN VIÊN (Staff Service)

#### 1️⃣ ĐĂNG NHẬP ADMIN/STAFF

**Đăng nhập:**
```
POST http://localhost:8003/api/staff-users/login/

Body:
{
    "username": "staff_user",
    "password": "securepass"
}

Response:
{
    "message": "Đăng nhập thành công",
    "token": "abc123...",
    "user": {
        "id": 1,
        "username": "staff_user",
        "role": "admin",
        "department": "IT Department"
    }
}
```

**Roles (Quyền):**
- `admin`: Quản trị viên - Full access
- `manager`: Quản lý - Có thể quản lý sách
- `editor`: Chỉnh sửa sách - Có thể thêm/sửa sách
- `viewer`: Xem - Chỉ xem

#### 2️⃣ QUẢN LÝ DANH MỤC SÁCH

**Xem danh sách sách (admin/manager/editor):**
```
GET http://localhost:8003/api/staff-books/list/

Header: Authorization: Token abc123...

Response:
{
    "message": "Danh sách sách",
    "total": 50,
    "books": [...]
}
```

#### 3️⃣ THÊM SÁCH MỚI

**Nhập sách mới:**
```
POST http://localhost:8003/api/staff-books/add/

Header: Authorization: Token abc123...

Body:
{
    "title": "New Django Book",
    "author": "New Author",
    "isbn": "978-1234567890",
    "description": "A comprehensive guide to Django",
    "genre": "science",
    "price": 39.99,
    "stock": 100,
    "publication_date": "2026-01-01",
    "publisher": "Tech Publisher",
    "pages": 500
}

Response:
{
    "message": "Sách đã được thêm thành công",
    "book": {
        "id": 51,
        "title": "New Django Book",
        ...
    }
}

Lưu ý: Staff profile sẽ cộng +1 vào books_added
```

#### 4️⃣ CHỈNH SỬA THÔNG TIN SÁCH

**Cập nhật thông tin sách (ví dụ: tên tác giả, giá):**
```
POST http://localhost:8003/api/staff-books/edit/

Header: Authorization: Token abc123...

Body:
{
    "book_id": 1,
    "title": "Django Advanced",
    "author": "Updated Author",
    "price": 49.99,
    "publisher": "New Publisher"
}

Response:
{
    "message": "Sách đã được cập nhật",
    "book": {...}
}

Lưu ý: Staff profile sẽ cộng +1 vào books_edited
```

#### 5️⃣ CẬP NHẬT TỒN KHO

**Tăng tồn kho (nhập hàng):**
```
POST http://localhost:8003/api/staff-books/update_stock/

Header: Authorization: Token abc123...

Body:
{
    "book_id": 1,
    "quantity": 50,
    "action": "increase"
}

Response:
{
    "message": "Tồn kho đã được increase 50 cuốn",
    "book": {
        "id": 1,
        "title": "...",
        "stock": 150  ← Cộng thêm 50
    }
}
```

**Giảm tồn kho (bán):**
```
POST http://localhost:8003/api/staff-books/update_stock/

Body:
{
    "book_id": 1,
    "quantity": 5,
    "action": "decrease"
}

Response:
{
    "message": "Tồn kho đã được decrease 5 cuốn",
    "book": {
        ...
        "stock": 145  ← Trừ 5
    }
}
```

#### 6️⃣ XEM BÁOCÁO

**Báo cáo quản lý sách:**
```
GET http://localhost:8003/api/staff-books/report/

Header: Authorization: Token abc123...

Response:
{
    "message": "Báo cáo quản lý sách",
    "book_stats": {
        "total_books": 50,
        "total_stock": 2500,
        "total_value": 125000.00,
        "average_price": 45.67,
        "books_out_of_stock": 3,
        "genres": [...]
    },
    "your_statistics": {
        "books_added": 15,
        "books_edited": 23
    }
}
```

---

## 🔄 FLOW - KHÁCH HÀNG MUA SÁCH

### Bước 1: Đăng ký/Đăng nhập
```powershell
POST /api/users/register/
→ Nhận token
```

### Bước 2: Tìm kiếm & xem sách
```powershell
GET /api/books/search/?q=django
GET /api/books/by_genre/?genre=science
GET /api/books/?min_price=20&max_price=50
```

### Bước 3: Thêm vào danh sách yêu thích
```powershell
POST /api/customers/{id}/add_to_favorites/
```

### Bước 4: Thêm vào giỏ hàng
```powershell
POST /api/carts/{customer_id}/add_item/
```

### Bước 5: Xem giỏ hàng
```powershell
GET /api/carts/{customer_id}/
```

### Bước 6: Tạo đơn hàng
```powershell
POST /api/orders/create/  (API Gateway)
```

---

## 🔄 FLOW - NHÂN VIÊN QUẢN LÝ SÁCH

### Bước 1: Đăng nhập
```powershell
POST /api/staff-users/login/
→ Nhận token
```

### Bước 2: Xem danh sách sách
```powershell
GET /api/staff-books/list/
```

### Bước 3: Thêm sách mới (khi nhập hàng)
```powershell
POST /api/staff-books/add/
```

### Bước 4: Cập nhật thông tin sách
```powershell
POST /api/staff-books/edit/
```

### Bước 5: Cập nhật tồn kho
```powershell
POST /api/staff-books/update_stock/
```

### Bước 6: Xem báo cáo
```powershell
GET /api/staff-books/report/
```

---

## 📦 CART SERVICE (PORT 8005)

**Service mới:** Quản lý giỏ hàng

**Models:**
- `Cart`: Giỏ hàng chính
- `CartItem`: Chi tiết sản phẩm trong giỏ

**Endpoints:**
- `GET /api/carts/{customer_id}/` - Lấy giỏ
- `POST /api/carts/{customer_id}/add_item/` - Thêm
- `POST /api/carts/{customer_id}/remove_item/` - Xóa
- `POST /api/carts/{customer_id}/update_quantity/` - Cập nhật số lượng
- `POST /api/carts/{customer_id}/clear/` - Xóa toàn bộ

---

## 🛠️ SETUP CART SERVICE

**1. Tạo service:**
```bash
django-admin startproject cart_service cart_service
cd cart_service
python manage.py startapp api
```

**2. Copy code:**
- `CART_SERVICE_models.py` → `api/models.py`
- `CART_SERVICE_serializers.py` → `api/serializers.py`
- `CART_SERVICE_views.py` → `api/views.py`
- `CART_SERVICE_urls.py` → `api/urls.py`

**3. Settings:**
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
```

**4. Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Run:**
```bash
python manage.py runserver 8005
```

---

## 📝 TỔNG HỢP CẬP NHẬT MODELS

### Customer Service
- `User` - Extended from AbstractUser (auth)
- `Customer` - Profile khách hàng

### Staff Service
- `StaffUser` - Extended from AbstractUser (auth)
- `Staff` - Profile nhân viên

### Book Service
- `Book` - Giữ nguyên (có thêm endpoints search)

### Cart Service (MỚI)
- `Cart` - Giỏ hàng
- `CartItem` - Chi tiết giỏ

### Order Service
- `Order` - Giữ nguyên
- `OrderItem` - Giữ nguyên

---

Chúc bạn thành công với tất cả chức năng mới! 🎉

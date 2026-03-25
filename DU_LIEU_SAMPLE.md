# =====================================================================
# DỮ LIỆU SAMPLE - NHẬP VÀO DATABASE ĐỂ KIỂM TRA
# =====================================================================

## Sử dụng Postman hoặc Insomnia - Lần lượt chạy các request sau

---

## 1. TẠO SÁCH (Book Service - POST http://localhost:8001/api/books/)

### Book 1:
```json
{
  "title": "Django for Beginners",
  "author": "William Vincent",
  "isbn": "978-1484222249",
  "description": "A step by step guide to learning Django web development",
  "genre": "science",
  "price": 29.99,
  "stock": 50,
  "publication_date": "2023-01-15",
  "publisher": "Packt Publishing",
  "pages": 400
}
```

### Book 2:
```json
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "isbn": "978-0132350884",
  "description": "A Handbook of Agile Software Craftsmanship",
  "genre": "science",
  "price": 35.99,
  "stock": 30,
  "publication_date": "2023-02-10",
  "publisher": "Prentice Hall",
  "pages": 464
}
```

### Book 3:
```json
{
  "title": "Python Crash Course",
  "author": "Eric Matthes",
  "isbn": "978-1593279288",
  "description": "A hands-on practical introduction to programming",
  "genre": "science",
  "price": 32.99,
  "stock": 45,
  "publication_date": "2023-03-05",
  "publisher": "No Starch Press",
  "pages": 544
}
```

### Book 4:
```json
{
  "title": "The Pragmatic Programmer",
  "author": "David Thomas, Andrew Hunt",
  "isbn": "978-0201616224",
  "description": "Your Journey to Mastery",
  "genre": "science",
  "price": 39.99,
  "stock": 25,
  "publication_date": "2023-04-01",
  "publisher": "Addison-Wesley",
  "pages": 352
}
```

### Book 5:
```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "978-0743273565",
  "description": "A beautiful story about the American Dream",
  "genre": "fiction",
  "price": 12.99,
  "stock": 60,
  "publication_date": "2023-05-20",
  "publisher": "Scribner",
  "pages": 180
}
```

---

## 2. TẠO KHÁCH HÀNG (Customer Service - POST http://localhost:8002/api/customers/)

### Customer 1:
```json
{
  "first_name": "Nguyễn",
  "last_name": "Văn An",
  "email": "nguyen.van.an@example.com",
  "phone": "0912345678",
  "address": "123 Đường Lê Lợi",
  "city": "Hà Nội",
  "postal_code": "10000",
  "country": "Việt Nam"
}
```

### Customer 2:
```json
{
  "first_name": "Trần",
  "last_name": "Thị Bình",
  "email": "tran.thi.binh@example.com",
  "phone": "0987654321",
  "address": "456 Đường Nguyễn Huệ",
  "city": "Thành phố Hồ Chí Minh",
  "postal_code": "70000",
  "country": "Việt Nam"
}
```

### Customer 3:
```json
{
  "first_name": "Phạm",
  "last_name": "Văn Tùng",
  "email": "pham.van.tung@example.com",
  "phone": "0909876543",
  "address": "789 Đường Tràng Triều",
  "city": "Đà Nẵng",
  "postal_code": "50000",
  "country": "Việt Nam"
}
```

---

## 3. TẠO NHÂN VIÊN (Staff Service - POST http://localhost:8003/api/staff/)

### Staff 1:
```json
{
  "first_name": "Lê",
  "last_name": "Minh Hoàng",
  "email": "le.minh.hoang@bookstore.com",
  "phone": "0343456789",
  "position": "manager",
  "salary": 5000000,
  "hire_date": "2022-01-15",
  "status": "active",
  "address": "111 Đường A",
  "city": "Hà Nội",
  "country": "Việt Nam"
}
```

### Staff 2:
```json
{
  "first_name": "Vũ",
  "last_name": "Thị Hương",
  "email": "vu.thi.huong@bookstore.com",
  "phone": "0376123456",
  "position": "seller",
  "salary": 3000000,
  "hire_date": "2023-02-01",
  "status": "active",
  "address": "222 Đường B",
  "city": "Hà Nội",
  "country": "Việt Nam"
}
```

### Staff 3:
```json
{
  "first_name": "Đinh",
  "last_name": "Văn Dũng",
  "email": "dinh.van.dung@bookstore.com",
  "phone": "0356789012",
  "position": "cashier",
  "salary": 2500000,
  "hire_date": "2023-03-10",
  "status": "active",
  "address": "333 Đường C",
  "city": "Hà Nội",
  "country": "Việt Nam"
}
```

---

## 4. TẠO ĐƠN HÀNG (Order Service - POST http://localhost:8004/api/orders/)

### Order 1:
```json
{
  "customer_id": 1,
  "total_amount": 74.97,
  "shipping_address": "123 Đường Lê Lợi, Hà Nội",
  "payment_method": "card",
  "payment_status": "unpaid"
}
```

### Order 2:
```json
{
  "customer_id": 2,
  "total_amount": 35.99,
  "shipping_address": "456 Đường Nguyễn Huệ, Thành phố Hồ Chí Minh",
  "payment_method": "online",
  "payment_status": "paid"
}
```

---

## 5. TẠO ĐƠN HÀNG THÔNG QUA API GATEWAY (QUY TRÌNH HOÀN CHỈNH)

### POST http://localhost:8000/api/orders/create/

```json
{
  "customer_id": 1,
  "items": [
    {
      "book_id": 1,
      "quantity": 2
    },
    {
      "book_id": 3,
      "quantity": 1
    }
  ],
  "shipping_address": "123 Đường Lê Lợi, Hà Nội",
  "payment_method": "card"
}
```

Quy trình này sẽ:
- ✅ Kiểm tra khách hàng tồn tại
- ✅ Kiểm tra sách tồn tại
- ✅ Kiểm tra tồn kho đủ
- ✅ Giảm tồn kho automation
- ✅ Tạo đơn hàng
- ✅ Cập nhật thống kê khách hàng

---

## 6. KIỂM TRA DỮ LIỆU

### Lấy danh sách sách (GET http://localhost:8001/api/books/)
```
Sẽ trả về danh sách 5 cuốn sách đã tạo
```

### Lấy danh sách khách hàng (GET http://localhost:8002/api/customers/)
```
Sẽ trả về danh sách 3 khách hàng đã tạo
```

### Lấy danh sách nhân viên (GET http://localhost:8003/api/staff/)
```
Sẽ trả về danh sách 3 nhân viên đã tạo
```

### Lấy danh sách đơn hàng (GET http://localhost:8004/api/orders/)
```
Sẽ trả về danh sách đơn hàng đã tạo
```

### Kiểm tra health (GET http://localhost:8000/api/health/)
```
Sẽ hiển thị trạng thái của tất cả services
```

---

## 7. LỌCP & FILTER

### Lọc sách theo thể loại:
```
GET http://localhost:8001/api/books/?genre=science
```

### Lọc khách hàng theo thành phố:
```
GET http://localhost:8002/api/customers/?city=Hà Nội
```

### Lấy 10 khách hàng chi tiêu nhiều nhất:
```
GET http://localhost:8002/api/customers/top_customers/
```

### Lấy sách còn hàng:
```
GET http://localhost:8001/api/books/available/
```

---

Chúc bạn kiểm tra thành công! 🎉

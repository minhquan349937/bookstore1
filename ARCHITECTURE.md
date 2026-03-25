# =====================================================================
# KIẾN TRÚC MICROSERVICES BOOKSTORE
# =====================================================================

## BIỂU ĐỒ KIẾN TRÚC

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser/Postman)               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  API GATEWAY (Port 8000)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  - api_root()                                            │  │
│  │  - health_check()                                        │  │
│  │  - create_order() [ORCHESTRATION]                        │  │
│  │    • Check customer exists                              │  │
│  │    • Check book exists & stock                          │  │
│  │    • Decrease book stock                                │  │
│  │    • Create order                                       │  │
│  │    • Update customer stats                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└──┬──────────────┬──────────────────┬──────────────────┬────────┘
   │              │                  │                  │
   ▼              ▼                  ▼                  ▼
┌────────┐    ┌──────────┐    ┌────────────┐    ┌────────────┐
│ BOOK   │    │CUSTOMER  │    │   STAFF    │    │   ORDER    │
│SERVICE │    │ SERVICE  │    │ SERVICE    │    │ SERVICE    │
│:8001   │    │  :8002   │    │   :8003    │    │   :8004    │
├────────┤    ├──────────┤    ├────────────┤    ├────────────┤
│ Books  │    │Customers │    │   Staff    │    │Orders      │
│ 📚     │    │ 👥       │    │   👔       │    │📦          │
├────────┤    ├──────────┤    ├────────────┤    ├────────────┤
│ Models:│    │ Models:  │    │ Models:    │    │ Models:    │
│ - Book │    │-Customer │    │ - Staff    │    │ - Order    │
│        │    │          │    │            │    │ - OrderItem│
├────────┤    ├──────────┤    ├────────────┤    ├────────────┤
│ CRUD:  │    │ CRUD:    │    │ CRUD:      │    │ CRUD:      │
│ /books│    │/customers│    │/staff      │    │/orders    │
│        │    │          │    │            │    │            │
│Custom: │    │Custom:   │    │Custom:     │    │Custom:     │
│/avilab│    │/top_...  │    │ (same as   │    │ (same as   │
│/decre..│    │/update_..│    │  Book)     │    │  Book)     │
│/incre..│    │          │    │            │    │            │
└────────┘    └──────────┘    └────────────┘    └────────────┘
   │              │                  │                  │
   │ SQLite       │ SQLite           │ SQLite           │ SQLite
   ▼ Database     ▼ Database         ▼ Database        ▼ Database
```

---

## QUY TRÌNH TẠO ĐƠN HÀNG (ORCHESTRATION)

```
CLIENT (Postman)
      │
      │ POST /api/orders/create/
      │ {customer_id: 1, items: [...], ...}
      │
      ▼
   Gateway (8000)
      │
      ├─► 1. Check Customer → Customer Service (8002) ✅
      │
      ├─► 2. For each item:
      │   a. Check Book → Book Service (8001) ✅
      │   b. Check Stock ✅
      │   c. POST decrease_stock → Book Service (8001) ✅
      │
      ├─► 3. Create Order → Order Service (8004) ✅
      │
      ├─► 4. Update customer stats → Customer Service (8002) ✅
      │
      └─► Return Order Response ✅
            {
              id: 1,
              order_number: "ORD-...",
              items: [...],
              total_amount: 100.00,
              ...
            }
```

---

## COMMUNICATION FLOW

```
┌─────────────────────────────────────────────────────────────┐
│ COMMUNICATION BETWEEN SERVICES                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Book Service ←──────► Customer Service                     │
│       ▲                      ▲                               │
│       │                      │                               │
│       └──►  API Gateway  ◄──┘                               │
│       ▲                      ▲                               │
│       │                      │                               │
│ Staff Service ◄────────► Order Service                     │
│                                                              │
│ METHOD: HTTP REST (requests library)                        │
│ FORMAT: JSON                                                │
│ CORS: Enabled                                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## DATABASE SCHEMA

### BOOK SERVICE (db.sqlite3)
```
Book
├── id (PK)
├── title
├── author
├── isbn (UNIQUE)
├── description
├── genre
├── price
├── stock
├── publication_date
├── publisher
├── pages
├── created_at
└── updated_at
```

### CUSTOMER SERVICE (db.sqlite3)
```
Customer
├── id (PK)
├── first_name
├── last_name
├── email (UNIQUE)
├── phone
├── address
├── city
├── postal_code
├── country
├── date_joined
├── last_login
├── is_active
├── total_orders
├── total_spent
├── created_at
└── updated_at
```

### STAFF SERVICE (db.sqlite3)
```
Staff
├── id (PK)
├── first_name
├── last_name
├── email (UNIQUE)
├── phone
├── position
├── salary
├── hire_date
├── status
├── address
├── city
├── country
├── created_at
└── updated_at
```

### ORDER SERVICE (db.sqlite3)
```
Order
├── id (PK)
├── customer_id (FK)
├── staff_id (FK, nullable)
├── order_number (UNIQUE)
├── order_date
├── total_amount
├── tax
├── discount
├── shipping_address
├── status
├── payment_method
├── payment_status
├── notes
├── created_at
└── updated_at

OrderItem
├── id (PK)
├── order_id (FK) → Order
├── book_id (FK)
├── book_title
├── quantity
├── unit_price
├── total_price
└── created_at
```

---

## API ENDPOINTS SUMMARY

```
┌─────────────────────────────────────────────────────────────┐
│                     API GATEWAY (8000)                      │
├─────────────────────────────────────────────────────────────┤
│ GET  /api/                           → API Root            │
│ GET  /api/health/                    → Health Check        │
│ POST /api/orders/create/             → Create Order (Orch) │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BOOK SERVICE (8001)                      │
├─────────────────────────────────────────────────────────────┤
│ GET    /api/books/                   → List Books          │
│ POST   /api/books/                   → Create Book         │
│ GET    /api/books/{id}/              → Get Book            │
│ PUT    /api/books/{id}/              → Update Book         │
│ DELETE /api/books/{id}/              → Delete Book         │
│ GET    /api/books/available/         → Available Books     │
│ POST   /api/books/{id}/decrease_stock/ → Decrease Stock   │
│ POST   /api/books/{id}/increase_stock/ → Increase Stock   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  CUSTOMER SERVICE (8002)                    │
├─────────────────────────────────────────────────────────────┤
│ GET    /api/customers/               → List Customers      │
│ POST   /api/customers/               → Create Customer     │
│ GET    /api/customers/{id}/          → Get Customer        │
│ PUT    /api/customers/{id}/          → Update Customer     │
│ DELETE /api/customers/{id}/          → Delete Customer     │
│ GET    /api/customers/top_customers/ → Top 10 Customers   │
│ POST   /api/customers/{id}/update_last_login/            │
│ POST   /api/customers/{id}/update_total_spent/           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    STAFF SERVICE (8003)                     │
├─────────────────────────────────────────────────────────────┤
│ GET    /api/staff/                   → List Staff          │
│ POST   /api/staff/                   → Create Staff        │
│ GET    /api/staff/{id}/              → Get Staff           │
│ PUT    /api/staff/{id}/              → Update Staff        │
│ DELETE /api/staff/{id}/              → Delete Staff        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    ORDER SERVICE (8004)                     │
├─────────────────────────────────────────────────────────────┤
│ GET    /api/orders/                  → List Orders         │
│ POST   /api/orders/                  → Create Order        │
│ GET    /api/orders/{id}/             → Get Order           │
│ PUT    /api/orders/{id}/             → Update Order        │
│ DELETE /api/orders/{id}/             → Delete Order        │
└─────────────────────────────────────────────────────────────┘
```

---

## TECHNOLOGY STACK

```
┌──────────────────────────────────────────────────────────────┐
│                   BOOKSTORE MICROSERVICES                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Backend Framework:    Django 4.2.10                         │
│  REST API:            Django REST Framework 3.14.0           │
│  Database:            SQLite (per service)                   │
│  CORS:               django-cors-headers 4.3.1              │
│  HTTP Client:         requests 2.31.0                        │
│                                                               │
│  Server:              Django Development Server             │
│  Ports:               8000-8004                              │
│                                                               │
│  API Style:           RESTful JSON API                       │
│  Authentication:      Can add JWT/Token later               │
│  Serialization:       JSON                                   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## DEPLOYMENT SEQUENCE

```
1. Run Setup Script
   └─► Create folder structure
       └─► 5 Django projects

2. Install Dependencies
   └─► pip install -r requirements.txt

3. Copy Code Files
   └─► 5 services × 4 files = 20 copy operations

4. Configure Each Service
   └─► settings.py
   └─► urls.py (project level)
   └─► urls.py (app level)

5. Database Setup
   └─► makemigrations
   └─► migrate
   └─► createsuperuser (for each)

6. Start Services
   └─► 5 terminals running simultaneously

7. Test with Postman
   └─► CRUD operations
   └─► Orchestration flows
```

---

Chúc bạn phát triển thành công! 🚀

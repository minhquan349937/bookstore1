# ============================================================
# Script khởi tạo Bookstore Microservices Platform
# Windows PowerShell
# ============================================================

$Green = 'Green'
$Yellow = 'Yellow'
$Red = 'Red'
$Cyan = 'Cyan'

function Write-Status {
    param([string]$Message, [string]$Color = $Green)
    Write-Host "==> $Message" -ForegroundColor $Color
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host "ERROR: $Message" -ForegroundColor $Red
}

try {
    # 1. Tạo thư mục chính
    Write-Status "Tạo cấu trúc Bookstore Microservices..." $Cyan
    $ProjectDir = "$PSScriptRoot\bookstore_microservices"
    
    if (Test-Path $ProjectDir) {
        Write-Status "Xóa cấu trúc cũ..." $Yellow
        Remove-Item $ProjectDir -Recurse -Force
    }
    
    New-Item -ItemType Directory -Path $ProjectDir -Force | Out-Null
    Set-Location $ProjectDir
    Write-Status "Thư mục tạo tại: $ProjectDir" $Green
    
    # 2. Danh sách các services
    $Services = @("api_gateway", "staff_service", "customer_service", "book_service", "order_service", "cart_service")
    
    # 3. Tạo từng service
    foreach ($Service in $Services) {
        Write-Status "Khởi tạo service: $Service" $Yellow
        
        # Tạo project Django
        django-admin startproject $Service $Service 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Project $Service tạo thành công!" $Green
            
            # Di chuyển vào project và tạo app
            Set-Location $Service
            python manage.py startapp api 2>$null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Status "App 'api' tạo thành công cho $Service!" $Green
            }
            
            Set-Location ..
        } else {
            Write-Error-Message "Lỗi khi tạo project $Service"
        }
    }
    
    Write-Status "====== HOÀN THÀNH ======" $Green
    Write-Host "`nCấu trúc đã tạo:`n" -ForegroundColor $Cyan
    Write-Host "bookstore_microservices/
├── api_gateway/
│   ├── api_gateway/
│   ├── api/
│   └── manage.py
├── staff_service/
│   ├── staff_service/
│   ├── api/
│   └── manage.py
├── customer_service/
│   ├── customer_service/
│   ├── api/
│   └── manage.py
├── book_service/
│   ├── book_service/
│   ├── api/
│   └── manage.py
├── order_service/
│   ├── order_service/
│   ├── api/
│   └── manage.py
└── cart_service/
    ├── cart_service/
    ├── api/
    └── manage.py
`n" -ForegroundColor $Cyan
    
} catch {
    Write-Error-Message "Lỗi xảy ra: $_"
    exit 1
}

Write-Status "Setup hoàn tất! Bắt đầu phát triển ứng dụng..." $Green

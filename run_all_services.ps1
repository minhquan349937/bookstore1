# ============================================================
# Run all Bookstore Microservices + Frontend
# ============================================================

$baseDir = "c:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01"
$venvDir = "$baseDir\.venv"
$servicesDir = "$baseDir\bookstore_microservices"
$frontendDir = "$baseDir\frontend"

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "BOOKSTORE MICROSERVICES STARTUP" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "[*] Activating Python virtual environment..." -ForegroundColor Green
& "$venvDir\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Install packages
Write-Host "[*] Installing dependencies..." -ForegroundColor Green
pip install -q -r "$baseDir\requirements.txt" 2>$null

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Starting Microservices..." -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# List of services with their ports
$services = @(
    @{Name="api_gateway"; Port=8000},
    @{Name="book_service"; Port=8001},
    @{Name="customer_service"; Port=8002},
    @{Name="staff_service"; Port=8003},
    @{Name="order_service"; Port=8004},
    @{Name="cart_service"; Port=8005}
)

# Start each service in a new PowerShell process
foreach ($service in $services) {
    $servicePath = "$servicesDir\$($service.Name)"
    $port = $service.Port
    $displayName = $service.Name -replace "_", " "
    
    Write-Host "[*] Starting $displayName on port $port..." -ForegroundColor Yellow
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", `
        "cd '$servicePath'; python manage.py runserver localhost:$port" `
        -WindowStyle Normal
    
    Start-Sleep -Milliseconds 800
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Starting Frontend Server..." -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Start frontend server on port 3000
Write-Host "[*] Starting frontend on port 3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$frontendDir'; python -m http.server 3000" `
    -WindowStyle Normal

Start-Sleep -Milliseconds 500

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "ALL SERVICES STARTED!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Cyan
Write-Host "   Customer UI:    http://localhost:3000/index.html" -ForegroundColor White
Write-Host "   Staff UI:       http://localhost:3000/staff/staff_login.html" -ForegroundColor White
Write-Host ""
Write-Host "Microservices:" -ForegroundColor Cyan
Write-Host "   API Gateway:     http://localhost:8000" -ForegroundColor White
Write-Host "   Book Service:    http://localhost:8001" -ForegroundColor White
Write-Host "   Customer Service: http://localhost:8002" -ForegroundColor White
Write-Host "   Staff Service:   http://localhost:8003" -ForegroundColor White
Write-Host "   Order Service:   http://localhost:8004" -ForegroundColor White
Write-Host "   Cart Service:    http://localhost:8005" -ForegroundColor White
Write-Host ""
Write-Host "Tips:" -ForegroundColor Yellow
Write-Host "   - Each service runs in a separate window" -ForegroundColor White
Write-Host "   - To stop all services, close each window or press Ctrl+C" -ForegroundColor White
Write-Host "   - Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan

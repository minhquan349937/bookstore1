# ============================================================
# Quick Docker Setup - Build and Run in Background
# ============================================================

$baseDir = "c:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01"

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Building and Starting Docker Services..." -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $baseDir

Write-Host "[1/3] Building Docker images..." -ForegroundColor Yellow
docker-compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/3] Starting services in background..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start services!" -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "[3/3] Checking service status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Docker Services Started Successfully!" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Cyan
Write-Host "  Customer UI:  http://localhost:3000/index.html" -ForegroundColor White
Write-Host "  Staff UI:     http://localhost:3000/staff/staff_login.html" -ForegroundColor White
Write-Host ""
Write-Host "View logs:" -ForegroundColor Cyan
Write-Host "  .\run_docker.ps1 logs" -ForegroundColor White
Write-Host ""
Write-Host "Stop services:" -ForegroundColor Cyan
Write-Host "  docker-compose down" -ForegroundColor White
Write-Host ""

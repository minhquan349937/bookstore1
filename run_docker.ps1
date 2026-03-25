# ============================================================
# Docker Compose Management Script
# ============================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$Command = "help"
)

$baseDir = "c:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01"

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Bookstore Microservices - Docker Manager" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

function Show-Help {
    Write-Host "Usage: .\run_docker.ps1 [command]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Cyan
    Write-Host "  build       - Build all Docker images" -ForegroundColor White
    Write-Host "  up          - Start all services" -ForegroundColor White
    Write-Host "  down        - Stop all services" -ForegroundColor White
    Write-Host "  restart     - Restart all services" -ForegroundColor White
    Write-Host "  logs        - View logs from all services" -ForegroundColor White
    Write-Host "  ps          - Show running containers" -ForegroundColor White
    Write-Host "  clean       - Remove all stopped containers and images" -ForegroundColor White
    Write-Host "  help        - Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\run_docker.ps1 build" -ForegroundColor Gray
    Write-Host "  .\run_docker.ps1 up" -ForegroundColor Gray
    Write-Host "  .\run_docker.ps1 logs" -ForegroundColor Gray
    Write-Host ""
}

try {
    Set-Location $baseDir
    
    switch ($Command.ToLower()) {
        "build" {
            Write-Host "[*] Building all Docker images..." -ForegroundColor Green
            docker-compose build
            Write-Host ""
            Write-Host "[OK] Build completed!" -ForegroundColor Green
        }
        
        "up" {
            Write-Host "[*] Starting all services..." -ForegroundColor Green
            Write-Host ""
            docker-compose up
            Write-Host ""
            Write-Host "[OK] Services started!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Access the application:" -ForegroundColor Cyan
            Write-Host "  Customer UI:  http://localhost:3000/index.html" -ForegroundColor White
            Write-Host "  Staff UI:     http://localhost:3000/staff/staff_login.html" -ForegroundColor White
        }
        
        "down" {
            Write-Host "[*] Stopping all services..." -ForegroundColor Yellow
            docker-compose down
            Write-Host ""
            Write-Host "[OK] Services stopped!" -ForegroundColor Green
        }
        
        "restart" {
            Write-Host "[*] Restarting all services..." -ForegroundColor Yellow
            docker-compose restart
            Write-Host ""
            Write-Host "[OK] Services restarted!" -ForegroundColor Green
        }
        
        "logs" {
            Write-Host "[*] Showing logs from all services..." -ForegroundColor Cyan
            Write-Host "Press Ctrl+C to stop viewing logs" -ForegroundColor Yellow
            Write-Host ""
            docker-compose logs -f
        }
        
        "ps" {
            Write-Host "[*] Running containers:" -ForegroundColor Cyan
            Write-Host ""
            docker-compose ps
        }
        
        "clean" {
            Write-Host "[*] Cleaning up Docker resources..." -ForegroundColor Yellow
            Write-Host "[*] Removing stopped containers..." -ForegroundColor Yellow
            docker-compose down -v
            Write-Host "[*] Removing unused images..." -ForegroundColor Yellow
            docker image prune -f
            Write-Host ""
            Write-Host "[OK] Cleanup completed!" -ForegroundColor Green
        }
        
        "help" {
            Show-Help
        }
        
        default {
            Write-Host "[ERROR] Unknown command: $Command" -ForegroundColor Red
            Write-Host ""
            Show-Help
        }
    }
}
catch {
    Write-Host "[ERROR] $($_)" -ForegroundColor Red
    exit 1
}

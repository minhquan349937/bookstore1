# Docker Setup Guide for Bookstore Microservices

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed (included with Docker Desktop)
- At least 4GB RAM available for Docker

## File Structure

```
kiemtra01/
├── docker-compose.yml          # Main orchestration file
├── .dockerignore               # Docker ignore patterns
├── bookstore_microservices/
│   ├── api_gateway/
│   │   └── Dockerfile
│   ├── book_service/
│   │   └── Dockerfile
│   ├── customer_service/
│   │   └── Dockerfile
│   ├── staff_service/
│   │   └── Dockerfile
│   ├── order_service/
│   │   └── Dockerfile
│   └── cart_service/
│       └── Dockerfile
└── frontend/                   # Frontend HTML/CSS/JS
```

## Quick Start with Docker Compose

### 1. Build all Docker images

```powershell
cd "c:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01"
docker-compose build
```

This will build all 6 microservice images + frontend.

### 2. Start all services

```powershell
docker-compose up
```

Or to run in background:

```powershell
docker-compose up -d
```

### 3. Access the application

- **Customer UI**: http://localhost:3000/index.html
- **Staff UI**: http://localhost:3000/staff/staff_login.html

### 4. Access microservices

- API Gateway: http://localhost:8000
- Book Service: http://localhost:8001
- Customer Service: http://localhost:8002
- Staff Service: http://localhost:8003
- Order Service: http://localhost:8004
- Cart Service: http://localhost:8005

### 5. Stop all services

```powershell
docker-compose down
```

## Individual Docker Commands

### Build a specific service

```powershell
docker-compose build book_service
```

### Start a specific service

```powershell
docker-compose up book_service
```

### View logs

```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f book_service
```

### Check running containers

```powershell
docker-compose ps
```

### Execute command in a running container

```powershell
docker-compose exec book_service python manage.py shell
```

## Troubleshooting

### Port already in use

If a port is already in use, modify the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "8001:8001"  # Change first number to different port
```

### Database connection issues

The current setup uses Django's SQLite database. Each container has its own database.
For production, configure PostgreSQL:

```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: bookstore
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Memory issues

Increase Docker Desktop memory allocation:
- Docker Desktop > Settings > Resources > Memory: Set to 4GB+

## Development Workflow

### Option 1: Using Docker Compose (Recommended)

```powershell
# Build
docker-compose build

# Run
docker-compose up

# In another terminal, make changes to code
# Changes will be visible in logs

# Stop
docker-compose down
```

### Option 2: Using PowerShell script (Current method)

```powershell
.\run_all_services.ps1
```

### Option 3: Manual Docker commands

```powershell
# Build individual service
docker build -t bookstore-book-service -f bookstore_microservices/book_service/Dockerfile .

# Run service
docker run -p 8001:8001 bookstore-book-service
```

## Production Deployment

For production deployment:

1. Remove `DEBUG=True` from environment variables
2. Add proper PostgreSQL database configuration
3. Use environment-specific docker-compose files:
   - `docker-compose.prod.yml`
   - `docker-compose.dev.yml`

4. Use proper secret management for credentials
5. Add health checks to services
6. Configure proper logging and monitoring

## Next Steps

1. Test the services: `docker-compose up`
2. Check logs: `docker-compose logs -f`
3. Verify all ports are accessible
4. Begin development with hot-reload enabled

## Support

For issues or questions:
1. Check service logs: `docker-compose logs [service-name]`
2. Verify network connectivity: `docker-compose exec [service] ping [other-service]`
3. Ensure all images are built: `docker-compose build --no-cache`

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project
COPY bookstore_microservices/customer_service .

# Expose port
EXPOSE 8002

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]

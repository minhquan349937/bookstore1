#!/usr/bin/env python
"""
Tạo cấu trúc Django hoàn chỉnh cho Bookstore Microservices
Tạo các file Django cần thiết thủ công
"""
import os
import shutil

BASE_DIR = r"c:\Users\Lenovo\OneDrive - ptit.edu.vn\Documents\kiemtra01\bookstore_microservices"
SERVICES = ["api_gateway", "staff_service", "customer_service", "book_service", "order_service", "cart_service"]

# Template các file Django
MANAGE_PY_TEMPLATE = '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{package_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''

INIT_PY = ''
SETTINGS_PY = '''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-fake-secret-key-for-development'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{package_name}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '{package_name}.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

CORS_ALLOWED_ORIGINS = {
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8000',
    'http://localhost:8001',
    'http://localhost:8002',
    'http://localhost:8003',
    'http://localhost:8004',
    'http://localhost:8005',
}
'''

URLS_PY = '''from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
'''

WSGI_PY = '''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{package_name}.settings')
application = get_wsgi_application()
'''

ASGI_PY = '''import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{package_name}.settings')
application = get_asgi_application()
'''

API_INIT_PY = ''

API_MODELS_PY = '''from django.db import models

# Create your models here.
'''

API_VIEWS_PY = '''from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def api_root(request):
    return Response({'message': 'Welcome to the API'})
'''

API_SERIALIZERS_PY = '''from rest_framework import serializers

# Create your serializers here.
'''

API_URLS_PY = '''from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
]

router = DefaultRouter()
urlpatterns += router.urls
'''

API_ADMIN_PY = '''from django.contrib import admin

# Register your models here.
'''

API_APPS_PY = '''from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
'''


def create_service_structure(service_name):
    """Tạo cấu trúc Django cho một service"""
    service_path = os.path.join(BASE_DIR, service_name)
    config_path = os.path.join(service_path, service_name)
    api_path = os.path.join(service_path, 'api')
    
    print(f"\n⏳ Khởi tạo: {service_name}")
    
    # Tạo các thư mục nếu chưa tồn tại
    os.makedirs(config_path, exist_ok=True)
    os.makedirs(api_path, exist_ok=True)
    
    # Tạo manage.py
    manage_py_path = os.path.join(service_path, 'manage.py')
    with open(manage_py_path, 'w') as f:
        f.write(MANAGE_PY_TEMPLATE.replace('{package_name}', service_name))
    
    # Tạo các file trong config folder
    with open(os.path.join(config_path, '__init__.py'), 'w') as f:
        f.write(INIT_PY)
    
    with open(os.path.join(config_path, 'settings.py'), 'w') as f:
        f.write(SETTINGS_PY.replace('{package_name}', service_name))
    
    with open(os.path.join(config_path, 'urls.py'), 'w') as f:
        f.write(URLS_PY)
    
    with open(os.path.join(config_path, 'wsgi.py'), 'w') as f:
        f.write(WSGI_PY.replace('{package_name}', service_name))
    
    with open(os.path.join(config_path, 'asgi.py'), 'w') as f:
        f.write(ASGI_PY.replace('{package_name}', service_name))
    
    # Tạo các file trong api folder
    with open(os.path.join(api_path, '__init__.py'), 'w') as f:
        f.write(API_INIT_PY)
    
    with open(os.path.join(api_path, 'models.py'), 'w') as f:
        f.write(API_MODELS_PY)
    
    with open(os.path.join(api_path, 'views.py'), 'w') as f:
        f.write(API_VIEWS_PY)
    
    with open(os.path.join(api_path, 'serializers.py'), 'w') as f:
        f.write(API_SERIALIZERS_PY)
    
    with open(os.path.join(api_path, 'urls.py'), 'w') as f:
        f.write(API_URLS_PY)
    
    with open(os.path.join(api_path, 'admin.py'), 'w') as f:
        f.write(API_ADMIN_PY)
    
    with open(os.path.join(api_path, 'apps.py'), 'w') as f:
        f.write(API_APPS_PY)
    
    print(f"✓ {service_name} khởi tạo thành công!")


def main():
    print("\n" + "="*60)
    print("🚀 KHỞI TẠO DJANGO MICROSERVICES")
    print("="*60)
    
    # Xóa cấu trúc cũ nếu tồn tại
    if os.path.exists(BASE_DIR):
        try:
            shutil.rmtree(BASE_DIR)
            print("✓ Xóa cấu trúc cũ")
        except Exception as e:
            print(f"⚠️  Không thể xóa cấu trúc cũ: {e}")
    
    # Tạo thư mục chính
    os.makedirs(BASE_DIR, exist_ok=True)
    
    # Tạo cấu trúc cho mỗi service
    for service in SERVICES:
        create_service_structure(service)
    
    print(f"\n{'='*60}")
    print(f"✓ HOÀN THÀNH!")
    print(f"{'='*60}")
    print(f"Cấu trúc đã tạo tại: {BASE_DIR}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

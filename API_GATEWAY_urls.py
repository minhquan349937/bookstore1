# api_gateway/urls.py

from django.contrib import admin
from django.urls import path, include
from api.views import api_root, health_check, create_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/health/', health_check, name='health-check'),
    path('api/orders/create/', create_order, name='create-order'),
]

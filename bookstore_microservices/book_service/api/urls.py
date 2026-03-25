from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')

urlpatterns = [
    path('', views.api_root, name='api-root'),
] + router.urls

# api/urls.py - STAFF SERVICE (Updated)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffUserViewSet, StaffBookManagementViewSet

router = DefaultRouter()
router.register(r'staff-users', StaffUserViewSet, basename='staff-user')
router.register(r'staff-books', StaffBookManagementViewSet, basename='staff-book')

urlpatterns = [
    path('', include(router.urls)),
]

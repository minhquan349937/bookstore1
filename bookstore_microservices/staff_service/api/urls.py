from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('staff-users/register/', views.staff_register, name='staff-register'),
    path('staff-users/login/', views.staff_login, name='staff-login'),
    path('staff-users/profile/', views.staff_profile, name='staff-profile'),
]

router = DefaultRouter()
urlpatterns += router.urls

from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('users/register/', views.register, name='register'),
    path('users/login/', views.login, name='login'),
    path('users/profile/', views.profile, name='profile'),
]

router = DefaultRouter()
urlpatterns += router.urls

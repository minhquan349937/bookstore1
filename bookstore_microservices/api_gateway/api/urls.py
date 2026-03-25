from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

urlpatterns = [
    path('', views.api_root, name='api-root'),
]

router = DefaultRouter()
urlpatterns += router.urls

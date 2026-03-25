from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('carts/<int:user_id>/', views.get_or_create_cart, name='get-cart'),
    path('carts/<int:user_id>/add_item/', views.add_to_cart, name='add-to-cart'),
    path('carts/<int:user_id>/remove_item/', views.remove_from_cart, name='remove-from-cart'),
    path('carts/<int:user_id>/update_quantity/', views.update_cart_quantity, name='update-quantity'),
    path('carts/<int:user_id>/clear_cart/', views.clear_cart, name='clear-cart'),
]

router = DefaultRouter()
urlpatterns += router.urls

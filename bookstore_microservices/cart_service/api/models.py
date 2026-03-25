from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user_id = models.IntegerField(unique=True)  # Foreign key dari Customer Service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for User {self.user_id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()  # Foreign key từ Book Service
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item {self.book_id} in Cart {self.cart.id}"

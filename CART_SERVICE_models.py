# api/models.py - CART SERVICE (SERVICE MỚI - Port 8005)

from django.db import models
from django.core.validators import MinValueValidator

class Cart(models.Model):
    """Model giỏ hàng của khách hàng"""
    
    customer_id = models.IntegerField(verbose_name="ID Khách hàng", unique=True)
    
    total_items = models.IntegerField(default=0, verbose_name="Tổng số mặt hàng")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Tổng giá"
    )
    
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Giỏ hàng"
        verbose_name_plural = "Giỏ hàng"
    
    def __str__(self):
        return f"Cart - Customer {self.customer_id}"


class CartItem(models.Model):
    """Model chi tiết mặt hàng trong giỏ hàng"""
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Giỏ hàng"
    )
    
    book_id = models.IntegerField(verbose_name="ID Sách")
    book_title = models.CharField(max_length=255, verbose_name="Tên sách")
    book_author = models.CharField(max_length=255, verbose_name="Tác giả")
    book_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Giá sách"
    )
    
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Số lượng"
    )
    
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Tổng tiền"
    )
    
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Mặt hàng trong giỏ"
        verbose_name_plural = "Mặt hàng trong giỏ"
        unique_together = ('cart', 'book_id')
    
    def save(self, *args, **kwargs):
        """Tự động tính subtotal"""
        self.subtotal = self.book_price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.book_title} x{self.quantity}"

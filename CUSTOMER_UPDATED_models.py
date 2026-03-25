# api/models.py - CUSTOMER SERVICE (Updated with Auth)

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Model User cho khách hàng"""
    USER_TYPE_CHOICES = [
        ('customer', 'Khách hàng'),
        ('staff', 'Nhân viên'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='customer',
        verbose_name="Loại người dùng"
    )
    
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, blank=True, verbose_name="Thành phố")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Mã bưu điện")
    country = models.CharField(max_length=100, default="Việt Nam", verbose_name="Quốc gia")
    
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    avatar = models.URLField(blank=True, verbose_name="Avatar")
    
    is_verified = models.BooleanField(default=False, verbose_name="Xác thực")
    
    total_orders = models.IntegerField(default=0, verbose_name="Tổng đơn hàng")
    total_spent = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Tổng chi tiêu"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
    
    def __str__(self):
        return self.username


class Customer(models.Model):
    """Model khách hàng (profile extends User)"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        verbose_name="Người dùng"
    )
    
    tier = models.CharField(
        max_length=20,
        choices=[
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum'),
        ],
        default='bronze',
        verbose_name="Tiers khách hàng"
    )
    
    loyalty_points = models.IntegerField(default=0, verbose_name="Điểm loyalty")
    
    favorite_books = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Danh sách sách yêu thích"
    )
    
    last_viewed_books = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Sách đã xem gần đây"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hồ sơ khách hàng"
        verbose_name_plural = "Hồ sơ khách hàng"
    
    def __str__(self):
        return f"Profile - {self.user.username}"

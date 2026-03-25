# api/models.py - CUSTOMER SERVICE

from django.db import models

class Customer(models.Model):
    """Model quản lý khách hàng"""
    
    first_name = models.CharField(max_length=100, verbose_name="Tên")
    last_name = models.CharField(max_length=100, verbose_name="Họ")
    
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    
    address = models.TextField(verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, verbose_name="Thành phố")
    postal_code = models.CharField(max_length=20, verbose_name="Mã bưu điện")
    country = models.CharField(max_length=100, verbose_name="Quốc gia")
    
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tham gia")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Lần đăng nhập cuối")
    
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    
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
        ordering = ['-date_joined']
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

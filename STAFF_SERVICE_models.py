# api/models.py - STAFF SERVICE

from django.db import models

class Staff(models.Model):
    """Model quản lý nhân viên"""
    
    POSITION_CHOICES = [
        ('manager', 'Quản lý'),
        ('seller', 'Nhân viên bán hàng'),
        ('cashier', 'Thu ngân'),
        ('warehouse', 'Kho hàng'),
        ('admin', 'Quản trị viên'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('on_leave', 'Đang nghỉ phép'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name="Tên")
    last_name = models.CharField(max_length=100, verbose_name="Họ")
    
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        verbose_name="Vị trí"
    )
    
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Lương"
    )
    
    hire_date = models.DateField(verbose_name="Ngày tuyển dụng")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Trạng thái"
    )
    
    address = models.TextField(verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, verbose_name="Thành phố")
    country = models.CharField(max_length=100, verbose_name="Quốc gia")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-hire_date']
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

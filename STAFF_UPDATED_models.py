# api/models.py - STAFF SERVICE (Updated with Auth)

from django.db import models
from django.contrib.auth.models import AbstractUser

class StaffUser(AbstractUser):
    """Model User cho nhân viên"""
    
    ROLE_CHOICES = [
        ('admin', 'Quản trị viên'),
        ('manager', 'Quản lý'),
        ('editor', 'Chỉnh sửa sách'),
        ('viewer', 'Xem'),
    ]
    
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='viewer',
        verbose_name="Vai trò"
    )
    
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Phòng ban"
    )
    
    hire_date = models.DateField(auto_now_add=True, verbose_name="Ngày tuyển dụng")
    
    is_active_staff = models.BooleanField(default=True, verbose_name="Nhân viên hoạt động")
    
    last_logged_in = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Lần đăng nhập cuối"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def has_perm_to_edit_books(self):
        """Kiểm tra quyền chỉnh sửa sách"""
        return self.role in ['admin', 'manager', 'editor']
    
    def has_perm_to_view_reports(self):
        """Kiểm tra quyền xem báo cáo"""
        return self.role in ['admin', 'manager']


class Staff(models.Model):
    """Model thông tin nhân viên"""
    
    user = models.OneToOneField(
        StaffUser,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        verbose_name="Người dùng"
    )
    
    position = models.CharField(
        max_length=100,
        verbose_name="Chức vụ"
    )
    
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Lương"
    )
    
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, blank=True, verbose_name="Thành phố")
    country = models.CharField(max_length=100, blank=True, verbose_name="Quốc gia")
    
    books_added = models.IntegerField(default=0, verbose_name="Số sách đã thêm")
    books_edited = models.IntegerField(default=0, verbose_name="Số sách đã chỉnh sửa")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hồ sơ nhân viên"
        verbose_name_plural = "Hồ sơ nhân viên"
    
    def __str__(self):
        return f"{self.user.username} - {self.position}"

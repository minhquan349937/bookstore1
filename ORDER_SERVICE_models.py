# api/models.py - ORDER SERVICE

from django.db import models
from django.utils import timezone

class Order(models.Model):
    """Model quản lý đơn hàng"""
    
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã gửi'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Tiền mặt'),
        ('card', 'Thẻ'),
        ('online', 'Thanh toán online'),
        ('transfer', 'Chuyển khoản'),
    ]
    
    # Khóa ngoại (lưu ID từ các services khác)
    customer_id = models.IntegerField(verbose_name="ID Khách hàng")
    staff_id = models.IntegerField(null=True, blank=True, verbose_name="ID Nhân viên")
    
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Số đơn hàng"
    )
    
    order_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày đặt hàng"
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Tổng tiền"
    )
    
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Thuế"
    )
    
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Giảm giá"
    )
    
    shipping_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Trạng thái"
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name="Phương thức thanh toán"
    )
    
    payment_status = models.CharField(
        max_length=20,
        choices=[('paid', 'Đã thanh toán'), ('unpaid', 'Chưa thanh toán')],
        default='unpaid',
        verbose_name="Trạng thái thanh toán"
    )
    
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_date']
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
    
    def __str__(self):
        return f"Đơn hàng {self.order_number}"
    
    def save(self, *args, **kwargs):
        """Tự động tạo số đơn hàng nếu chưa có"""
        if not self.order_number:
            from django.utils.text import slugify
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.order_number = f"ORD-{timestamp}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Model chi tiết mặt hàng trong đơn hàng"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Đơn hàng"
    )
    
    book_id = models.IntegerField(verbose_name="ID Sách")
    book_title = models.CharField(
        max_length=255,
        verbose_name="Tên sách"
    )
    
    quantity = models.IntegerField(verbose_name="Số lượng")
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Giá đơn vị"
    )
    
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Tổng giá"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"
    
    def __str__(self):
        return f"{self.book_title} - {self.quantity}x"

# books/models.py - BOOK SERVICE

from django.db import models

class Book(models.Model):
    """Model quản lý các cuốn sách"""
    GENRE_CHOICES = [
        ('fiction', 'Tiểu thuyết'),
        ('non-fiction', 'Phi hư cấu'),
        ('science', 'Khoa học'),
        ('history', 'Lịch sử'),
        ('self-help', 'Tự giúp'),
        ('children', 'Trẻ em'),
    ]
    
    title = models.CharField(max_length=255, verbose_name="Tên sách")
    author = models.CharField(max_length=255, verbose_name="Tác giả")
    isbn = models.CharField(max_length=20, unique=True, verbose_name="ISBN")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    genre = models.CharField(
        max_length=50, 
        choices=GENRE_CHOICES,
        verbose_name="Thể loại"
    )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Giá tiền"
    )
    
    stock = models.IntegerField(default=0, verbose_name="Số lượng tồn kho")
    
    publication_date = models.DateField(verbose_name="Ngày xuất bản")
    publisher = models.CharField(max_length=255, verbose_name="Nhà xuất bản")
    
    pages = models.IntegerField(verbose_name="Số trang")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sách"
        verbose_name_plural = "Sách"
    
    def __str__(self):
        return f"{self.title} - {self.author}"

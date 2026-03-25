from django.db import models
from django.contrib.auth.models import User

class Laptop(models.Model):
    BRAND_CHOICES = [
        ('Apple', 'Apple'),
        ('Dell', 'Dell'),
        ('HP', 'HP'),
        ('Lenovo', 'Lenovo'),
        ('ASUS', 'ASUS'),
        ('Acer', 'Acer'),
        ('MSI', 'MSI'),
        ('Razer', 'Razer'),
    ]

    CATEGORY_CHOICES = [
        ('Gaming', 'Gaming'),
        ('Ultrabook', 'Ultrabook'),
        ('Business', 'Business'),
        ('Student', 'Student'),
        ('Workstation', 'Workstation'),
    ]

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    model_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    processor = models.CharField(max_length=200)
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    display = models.CharField(max_length=100)
    gpu = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.name} ({self.model_name})"

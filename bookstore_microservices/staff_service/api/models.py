from django.db import models
from django.contrib.auth.models import User

class Staff(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='librarian')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

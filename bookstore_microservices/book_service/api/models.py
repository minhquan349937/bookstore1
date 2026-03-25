from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Mystery', 'Mystery'),
        ('Science Fiction', 'Science Fiction'),
        ('Romance', 'Romance'),
        ('Biography', 'Biography'),
        ('History', 'History'),
        ('Technology', 'Technology'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    year = models.IntegerField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

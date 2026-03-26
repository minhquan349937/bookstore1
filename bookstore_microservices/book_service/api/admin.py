from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publisher', 'genre', 'price', 'stock', 'created_at')
    list_filter = ('genre', 'year', 'created_at')
    search_fields = ('title', 'author', 'publisher', 'isbn')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'author', 'publisher', 'isbn')
        }),
        ('Chi tiết sách', {
            'fields': ('genre', 'year', 'pages', 'description')
        }),
        ('Giá & Kho', {
            'fields': ('price', 'stock')
        }),
        ('Hình ảnh & Thời gian', {
            'fields': ('cover_image', 'created_at', 'updated_at')
        }),
    )

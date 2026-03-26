from django.contrib import admin
from .models import Laptop

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'name', 'model_name', 'category', 'processor', 'ram', 'price', 'stock')
    list_filter = ('brand', 'category', 'created_at')
    search_fields = ('name', 'brand', 'model_name', 'processor')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'brand', 'model_name', 'category')
        }),
        ('Cấu hình kỹ thuật', {
            'fields': ('processor', 'ram', 'storage', 'display', 'gpu')
        }),
        ('Giá & Kho', {
            'fields': ('price', 'stock')
        }),
        ('Mô tả & Hình ảnh', {
            'fields': ('description', 'image', 'created_at', 'updated_at')
        }),
    )

from django.contrib import admin
from .models import Mobile

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'name', 'model_name', 'os', 'processor', 'ram', 'price', 'stock')
    list_filter = ('brand', 'os', 'created_at')
    search_fields = ('name', 'brand', 'model_name', 'processor')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'brand', 'model_name', 'os')
        }),
        ('Cấu hình kỹ thuật', {
            'fields': ('processor', 'ram', 'storage', 'display', 'camera', 'battery')
        }),
        ('Giá & Kho', {
            'fields': ('price', 'stock')
        }),
        ('Mô tả & Hình ảnh', {
            'fields': ('description', 'image', 'created_at', 'updated_at')
        }),
    )

from django.contrib import admin
from .models import Category, Product, Cart, ProductImage

# Inline для дополнительных изображений
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # по умолчанию одно пустое поле для загрузки

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'available', 'category', 'main_image')
    list_filter = ('available', 'category')
    search_fields = ('title', 'description')
    inlines = [ProductImageInline]

# Остальные модели регистрируем стандартно
admin.site.register(Category)
admin.site.register(Cart)

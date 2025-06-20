from django.contrib import admin
from .models import Category, Product, Cart, ProductImage, Size

# Inline для дополнительных изображений
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'available', 'category', 'main_image')
    list_filter  = ('available', 'category', 'color', 'sizes')
    search_fields = ('title', 'description')
    inlines = [ProductImageInline]
    filter_horizontal = ('sizes',)

admin.site.register(Category)
admin.site.register(Cart)

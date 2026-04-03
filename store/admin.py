from django.contrib import admin
from .models import Category, Book, Order, Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    list_editable = ['price', 'stock', 'is_active']
    search_fields = ['title', 'author']

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)

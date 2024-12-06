from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'rating', 'is_best_deal')
    list_filter = ('is_best_deal', 'discount', 'rating')
    search_fields = ('name',)

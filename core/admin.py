from django.contrib import admin
from .models import Location, Category


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "city", "area", "show_approximate_only")
    list_filter = ("city",)
    search_fields = ("city", "area", "address_line")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type", "slug")
    list_filter = ("category_type",)
    prepopulated_fields = {"slug": ("name",)}

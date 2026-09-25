from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "city", "joined_at")
    list_filter = ("role", "city")
    search_fields = ("user__username", "user__email", "city")

from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("campaign", "donor", "amount", "category", "status", "created_at")
    list_filter = ("status", "category", "campaign")

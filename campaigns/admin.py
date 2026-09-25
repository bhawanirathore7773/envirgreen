from django.contrib import admin
from .models import Campaign, CampaignMember


class CampaignMemberInline(admin.TabularInline):
    model = CampaignMember
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "campaign_type", "location", "progress_count", "goal_count", "is_active", "start_date")
    list_filter = ("campaign_type", "is_active")
    search_fields = ("title", "objective")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CampaignMemberInline]

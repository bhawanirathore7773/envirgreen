from django.contrib import admin
from .models import Issue, IssueUpdate


class IssueUpdateInline(admin.TabularInline):
    model = IssueUpdate
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "severity", "location", "created_at")
    list_filter = ("status", "severity", "category", "is_recurring")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [IssueUpdateInline]


@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ("issue", "status", "actor", "created_at")
    list_filter = ("status",)

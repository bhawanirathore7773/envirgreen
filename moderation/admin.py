from django.contrib import admin
from .models import ContentReport, AuditLog


@admin.register(ContentReport)
class ContentReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reporter", "content_type", "reason", "status", "created_at")
    list_filter = ("status", "reason", "content_type")
    actions = ["mark_approved", "mark_rejected", "mark_removed"]

    @admin.action(description="Mark selected reports as approved")
    def mark_approved(self, request, queryset):
        queryset.update(status="approved", reviewed_by=request.user)

    @admin.action(description="Mark selected reports as rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(status="rejected", reviewed_by=request.user)

    @admin.action(description="Remove reported content's visibility")
    def mark_removed(self, request, queryset):
        queryset.update(status="removed", reviewed_by=request.user)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "action", "object_repr")
    list_filter = ("action",)
    search_fields = ("object_repr", "action")
    readonly_fields = [f.name for f in AuditLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

from django.contrib import admin
from .models import ImpactSnapshot


@admin.register(ImpactSnapshot)
class ImpactSnapshotAdmin(admin.ModelAdmin):
    list_display = ("city", "trees_planted", "cleanup_drives", "issues_resolved", "generated_at")
    readonly_fields = [f.name for f in ImpactSnapshot._meta.fields]

    def has_add_permission(self, request):
        return False

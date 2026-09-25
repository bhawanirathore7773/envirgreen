from django.contrib import admin
from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "campaign", "location", "start_time", "registered_count", "capacity")
    list_filter = ("campaign",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EventRegistrationInline]


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "attended", "registered_at")
    list_filter = ("attended",)
    actions = ["mark_attended"]

    @admin.action(description="Mark selected registrations as attended")
    def mark_attended(self, request, queryset):
        queryset.update(attended=True)

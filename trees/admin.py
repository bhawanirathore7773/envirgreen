from django.contrib import admin
from .models import TreePlantation, TreeVerification


class TreeVerificationInline(admin.TabularInline):
    model = TreeVerification
    extra = 0


@admin.register(TreePlantation)
class TreePlantationAdmin(admin.ModelAdmin):
    list_display = ("species", "count", "planter", "location", "status", "planted_on")
    list_filter = ("status", "species")
    inlines = [TreeVerificationInline]

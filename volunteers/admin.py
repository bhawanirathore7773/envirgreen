from django.contrib import admin
from .models import Skill, Volunteer


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("user", "mobile", "availability", "age_group", "registered_at")
    list_filter = ("availability", "age_group", "skills")
    filter_horizontal = ("skills",)

from django.contrib import admin
from .models import Post, Reaction, Comment, SavedPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "post_type", "is_approved", "is_verified", "created_at")
    list_filter = ("post_type", "is_approved", "is_verified")
    actions = ["approve_posts"]

    @admin.action(description="Approve selected posts for the public feed")
    def approve_posts(self, request, queryset):
        queryset.update(is_approved=True)


admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(SavedPost)

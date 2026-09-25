from django.conf import settings
from django.db import models

from campaigns.models import Campaign
from core.models import Location


class Post(models.Model):
    POST_TYPES = [
        ("report", "Report"),
        ("achievement", "Achievement"),
        ("action", "Action"),
        ("awareness", "Awareness"),
        ("campaign", "Campaign"),
        ("appreciation", "Appreciation"),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    text = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    is_verified = models.BooleanField(default=False, help_text="Set once moderation confirms this is genuine.")
    is_approved = models.BooleanField(default=False, help_text="Must be true to appear in the public feed.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_post_type_display()} by {self.author}"

    @property
    def appreciation_count(self):
        return self.reactions.count()


class Reaction(models.Model):
    REACTION_CHOICES = [
        ("green_action", "🌱 Green Action"),
        ("clean_action", "🧹 Clean Action"),
        ("tree_champion", "🌳 Tree Champion"),
        ("community_support", "💚 Community Support"),
        ("inspiration", "👏 Inspiration"),
    ]

    post = models.ForeignKey(Post, related_name="reactions", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class SavedPost(models.Model):
    post = models.ForeignKey(Post, related_name="saved_by", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_posts")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

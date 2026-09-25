from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import Location
from issues.models import Issue


class Campaign(models.Model):
    TYPE_CHOICES = [
        ("river_cleanup", "River Cleanup"),
        ("lake_cleanup", "Lake Cleanup"),
        ("street_cleanup", "Street Cleanup"),
        ("tree_plantation", "Tree Plantation"),
        ("plastic_free", "Plastic-Free Campaign"),
        ("school_awareness", "School Awareness"),
        ("college_awareness", "College Awareness"),
        ("waste_segregation", "Waste Segregation"),
        ("public_awareness", "Public Awareness"),
        ("urban_plantation", "Urban Plantation"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    campaign_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    objective = models.TextField()
    cover_photo = models.ImageField(upload_to="campaigns/", blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    related_issue = models.ForeignKey(Issue, null=True, blank=True, on_delete=models.SET_NULL, related_name="campaigns")
    goal_count = models.PositiveIntegerField(default=1, help_text="e.g. number of cleanup drives targeted")
    progress_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:180]
            slug = base
            i = 1
            while Campaign.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("campaigns:detail", kwargs={"slug": self.slug})

    @property
    def progress_percent(self):
        return min(100, int((self.progress_count / self.goal_count) * 100)) if self.goal_count else 0

    @property
    def volunteer_count(self):
        return self.members.filter(support_type="volunteer").count()


class CampaignMember(models.Model):
    SUPPORT_TYPES = [
        ("volunteer", "Volunteer"),
        ("financial", "Financial"),
        ("material", "Material"),
        ("skills", "Skills"),
    ]

    campaign = models.ForeignKey(Campaign, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campaign_memberships")
    support_type = models.CharField(max_length=20, choices=SUPPORT_TYPES)
    detail = models.CharField(max_length=255, blank=True, help_text="e.g. 'Can provide gloves and water'")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("campaign", "user", "support_type")
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user} → {self.campaign} ({self.get_support_type_display()})"

from django.conf import settings
from django.db import models

from core.models import Location


class TreePlantation(models.Model):
    STATUS_CHOICES = [
        ("planted", "Planted"),
        ("verified", "Verified"),
        ("growing", "Growing"),
        ("survived", "Survived"),
    ]

    planter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="tree_plantations"
    )
    species = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to="trees/", blank=True, null=True)
    organisation = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="planted")
    planted_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-planted_on"]

    def __str__(self):
        return f"{self.count} × {self.species} — {self.get_status_display()}"


class TreeVerification(models.Model):
    tree = models.ForeignKey(TreePlantation, related_name="checkins", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=TreePlantation.STATUS_CHOICES)
    photo = models.ImageField(upload_to="tree_checkins/", blank=True, null=True)
    note = models.CharField(max_length=255, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Keep the parent tree's status in sync with its latest check-in.
        self.tree.status = self.status
        self.tree.save(update_fields=["status"])

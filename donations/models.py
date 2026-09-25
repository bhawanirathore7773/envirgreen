from django.conf import settings
from django.db import models

from campaigns.models import Campaign

SPEND_CATEGORY_CHOICES = [
    ("plantation", "Plantation"),
    ("cleanup_equipment", "Cleanup Equipment"),
    ("awareness", "Awareness Campaigns"),
    ("volunteer_activities", "Volunteer Activities"),
    ("community_programs", "Community Programs"),
    ("technology", "Technology"),
    ("operations", "Operations"),
]


class Donation(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed"), ("refunded", "Refunded")]

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="donations")
    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT, related_name="donations")
    category = models.CharField(max_length=30, choices=SPEND_CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    gateway_txn_id = models.CharField(max_length=100, blank=True, unique=False)
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"₹{self.amount} — {self.campaign} ({self.get_status_display()})"

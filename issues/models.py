from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import Location, Category


class Issue(models.Model):
    """An environmental/civic issue reported by a citizen.

    See docs/02-core-platform-systems.md, "Environmental Issue Reporting
    System" for the full status-pipeline rationale.
    """

    STATUS_CHOICES = [
        ("reported", "Reported"),
        ("verified", "Verified"),
        ("authority_identified", "Authority Identified"),
        ("reported_to_authority", "Reported to Authority"),
        ("followup_required", "Follow-up Required"),
        ("action_taken", "Action Taken"),
        ("community_verified", "Community Verification"),
        ("resolved", "Resolved"),
        ("escalated", "Escalated"),
        ("no_action", "No Action"),
    ]
    SEVERITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, limit_choices_to={"category_type": "issue"})
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="reported_issues"
    )
    description = models.TextField()
    photo = models.ImageField(upload_to="issues/", blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="medium")
    is_recurring = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="reported")
    responsible_authority_category = models.CharField(max_length=150, blank=True)
    supporter_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"]), models.Index(fields=["-created_at"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:180]
            slug = base
            i = 1
            while Issue.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("issues:detail", kwargs={"slug": self.slug})

    # The "happy path" sequence shown on the public status stepper.
    # escalated/no_action are shown separately, not as steps on this line.
    PIPELINE_ORDER = [
        "reported", "verified", "authority_identified", "reported_to_authority",
        "followup_required", "action_taken", "community_verified", "resolved",
    ]

    def pipeline_steps(self):
        labels = dict(self.STATUS_CHOICES)
        try:
            current_index = self.PIPELINE_ORDER.index(self.status)
        except ValueError:
            current_index = -1  # status is escalated/no_action — off the happy path
        steps = []
        for i, key in enumerate(self.PIPELINE_ORDER):
            if current_index == -1:
                state = ""
            elif i < current_index:
                state = "done"
            elif i == current_index:
                state = "current"
            else:
                state = ""
            steps.append({"label": labels[key], "state": state})
        return steps


class IssueUpdate(models.Model):
    """One entry in an issue's public timeline. Created only through
    issues.services.transition_issue — never edited directly in a view —
    so every status change is audited (see AuditLog in moderation app)."""

    issue = models.ForeignKey(Issue, related_name="timeline", on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=Issue.STATUS_CHOICES)
    note = models.TextField(blank=True)
    photo = models.ImageField(upload_to="issue_updates/", blank=True, null=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.issue.title} → {self.get_status_display()}"

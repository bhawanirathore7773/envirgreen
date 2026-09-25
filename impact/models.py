from django.db import models


class ImpactSnapshot(models.Model):
    """A dated, computed snapshot of platform-wide impact numbers.

    Written by impact.services.recompute_impact_snapshot (intended to run
    nightly via Celery beat in production). The public dashboard reads the
    latest snapshot instead of running expensive live aggregation on every
    page view — see docs/03-technical-architecture.md, Performance.
    """

    city = models.CharField(max_length=100, blank=True, help_text="Blank = platform-wide")
    trees_planted = models.PositiveIntegerField(default=0)
    trees_survived = models.PositiveIntegerField(default=0)
    cleanup_drives = models.PositiveIntegerField(default=0)
    waste_collected_kg = models.PositiveIntegerField(default=0)
    active_volunteers = models.PositiveIntegerField(default=0)
    issues_reported = models.PositiveIntegerField(default=0)
    issues_resolved = models.PositiveIntegerField(default=0)
    institutions_reached = models.PositiveIntegerField(default=0)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"Snapshot ({self.city or 'platform-wide'}) — {self.generated_at:%Y-%m-%d}"

    @property
    def survival_rate_percent(self):
        return round((self.trees_survived / self.trees_planted) * 100) if self.trees_planted else 0

    @property
    def resolution_rate_percent(self):
        return round((self.issues_resolved / self.issues_reported) * 100) if self.issues_reported else 0

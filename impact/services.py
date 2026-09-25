"""Impact aggregation. In production, recompute_impact_snapshot runs on a
nightly Celery beat schedule and writes an ImpactSnapshot row; the
dashboard reads that cached row. This scaffold computes live for
simplicity — swap get_impact_snapshot() to read the latest ImpactSnapshot
once Celery is wired up.
"""

from trees.models import TreePlantation
from issues.models import Issue
from campaigns.models import CampaignMember
from events.models import EventRegistration

from .models import ImpactSnapshot


def recompute_impact_snapshot(city: str = "") -> ImpactSnapshot:
    trees = TreePlantation.objects.all()
    issues = Issue.objects.all()
    if city:
        trees = trees.filter(location__city__iexact=city)
        issues = issues.filter(location__city__iexact=city)

    return ImpactSnapshot.objects.create(
        city=city,
        trees_planted=sum(trees.values_list("count", flat=True)),
        trees_survived=sum(trees.filter(status="survived").values_list("count", flat=True)),
        cleanup_drives=EventRegistration.objects.filter(attended=True).values("event").distinct().count(),
        waste_collected_kg=0,  # populate from CleanupActivity records once that model is in use
        active_volunteers=CampaignMember.objects.filter(support_type="volunteer").values("user").distinct().count(),
        issues_reported=issues.count(),
        issues_resolved=issues.filter(status="resolved").count(),
        institutions_reached=0,
    )


def get_impact_snapshot(city: str = ""):
    """Fast path for template rendering — computes on the fly for this
    scaffold. Swap for `ImpactSnapshot.objects.filter(city=city).first()`
    once the nightly Celery task is running."""
    return recompute_impact_snapshot(city)

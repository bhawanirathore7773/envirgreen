"""Feed ranking — prioritizes verified action over raw engagement counts.

Deliberately NOT sorted by like-count or comment-count: see
docs/02-core-platform-systems.md, "Community / Social System" for why an
outrage-optimized feed is exactly what this platform must avoid.
"""

from django.db.models import Case, When, IntegerField, F
from django.utils import timezone

from .models import Post

TYPE_WEIGHT = {
    "achievement": 5,
    "campaign": 4,
    "report": 3,
    "awareness": 2,
    "action": 3,
    "appreciation": 1,
}


def rank_feed():
    qs = Post.objects.filter(is_approved=True).select_related("author", "author__profile", "campaign")
    whens = [When(post_type=k, then=v) for k, v in TYPE_WEIGHT.items()]
    qs = qs.annotate(
        type_weight=Case(*whens, default=1, output_field=IntegerField()),
        verified_weight=Case(When(is_verified=True, then=3), default=0, output_field=IntegerField()),
    )
    # Recency-weighted within tiers rather than a pure engagement sort.
    return qs.order_by("-verified_weight", "-type_weight", "-created_at")

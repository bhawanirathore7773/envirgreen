from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from campaigns.models import Campaign
from issues.models import Issue
from impact.services import get_impact_snapshot


def home(request):
    active_campaigns = Campaign.objects.filter(is_active=True).select_related("location")[:6]
    recent_issues = Issue.objects.select_related("location", "category").order_by("-created_at")[:4]
    snapshot = get_impact_snapshot()
    context = {
        "active_campaigns": active_campaigns,
        "recent_issues": recent_issues,
        "snapshot": snapshot,
    }
    return render(request, "core/home.html", context)


def about(request):
    return render(request, "core/about.html")


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == "POST":
        # In production: validate via a Django form, send async via Celery,
        # and apply spam protection (honeypot field / rate limiting).
        messages.success(request, "Thanks — your message has been sent to the Envirgreen team.")
        return redirect("core:contact")
    return render(request, "core/contact.html")


def take_action(request):
    """The 'Take Action' wizard landing — routes to the right flow."""
    return render(request, "core/take_action.html")

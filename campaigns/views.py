from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Campaign, CampaignMember


def campaign_list(request):
    campaigns = Campaign.objects.filter(is_active=True).select_related("location")
    return render(request, "campaigns/list.html", {"campaigns": campaigns})


def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign.objects.select_related("location", "organizer"), slug=slug)
    already_joined = (
        campaign.members.filter(user=request.user).exists() if request.user.is_authenticated else False
    )
    return render(request, "campaigns/detail.html", {"campaign": campaign, "already_joined": already_joined})


@login_required
def join_campaign(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    support_type = request.POST.get("support_type", "volunteer")
    detail = request.POST.get("detail", "")
    CampaignMember.objects.get_or_create(
        campaign=campaign, user=request.user, support_type=support_type, defaults={"detail": detail}
    )
    messages.success(request, f"You're in — thanks for joining {campaign.title}.")
    return redirect(campaign.get_absolute_url())

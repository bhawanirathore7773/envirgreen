from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from campaigns.models import Campaign
from .forms import DonationForm


@login_required
def donate(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.campaign = campaign
            donation.donor = request.user
            # NOTE: payment gateway integration (e.g. Razorpay) goes here —
            # this scaffold records the intent; wire up a real charge +
            # webhook before accepting real money. See docs/03-technical-
            # architecture.md, "Final Recommended Technology Stack".
            donation.status = "pending"
            donation.save()
            messages.success(request, "Thank you — redirecting you to complete payment.")
            return redirect(campaign.get_absolute_url())
    else:
        form = DonationForm()
    return render(request, "donations/donate.html", {"form": form, "campaign": campaign})

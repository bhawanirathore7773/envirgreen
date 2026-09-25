from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from campaigns.models import CampaignMember
from events.models import EventRegistration
from .forms import VolunteerRegistrationForm
from .models import Volunteer


def register(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    if hasattr(request.user, "volunteer_profile"):
        return redirect("volunteers:dashboard")
    if request.method == "POST":
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.user = request.user
            volunteer.save()
            form.save_m2m()
            request.user.profile.role = "verified_volunteer"
            request.user.profile.save(update_fields=["role"])
            messages.success(request, "Welcome aboard — we'll match you to a nearby campaign soon.")
            return redirect("volunteers:dashboard")
    else:
        form = VolunteerRegistrationForm()
    return render(request, "volunteers/register.html", {"form": form})


@login_required
def dashboard(request):
    upcoming_events = EventRegistration.objects.filter(user=request.user).select_related("event")
    campaigns = CampaignMember.objects.filter(user=request.user).select_related("campaign")
    return render(
        request, "volunteers/dashboard.html", {"upcoming_events": upcoming_events, "campaigns": campaigns}
    )

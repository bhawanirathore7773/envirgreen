from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Event, EventRegistration


def event_list(request):
    events = Event.objects.select_related("location", "campaign")
    return render(request, "events/list.html", {"events": events})


def event_detail(request, slug):
    event = get_object_or_404(Event.objects.select_related("location", "campaign", "organizer"), slug=slug)
    is_registered = event.registrations.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, "events/detail.html", {"event": event, "is_registered": is_registered})


@login_required
def register_for_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    EventRegistration.objects.get_or_create(event=event, user=request.user)
    messages.success(request, f"You're registered for {event.title}.")
    return redirect(event.get_absolute_url())

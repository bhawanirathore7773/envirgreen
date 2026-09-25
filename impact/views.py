from django.shortcuts import render
from .services import get_impact_snapshot


def dashboard(request):
    city = request.GET.get("city", "")
    snapshot = get_impact_snapshot(city)
    return render(request, "impact/dashboard.html", {"snapshot": snapshot, "city": city})

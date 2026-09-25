from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone


@login_required
def inbox(request):
    notifications = request.user.notifications.all()[:50]
    request.user.notifications.filter(read_at__isnull=True).update(read_at=timezone.now())
    return render(request, "notifications/inbox.html", {"notifications": notifications})

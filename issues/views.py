from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import IssueReportForm
from .models import Issue


def issue_list(request):
    status = request.GET.get("status", "")
    issues = Issue.objects.select_related("category", "location")
    if status:
        issues = issues.filter(status=status)
    return render(
        request,
        "issues/list.html",
        {"issues": issues, "status_choices": Issue.STATUS_CHOICES, "selected_status": status},
    )


def issue_detail(request, slug):
    issue = get_object_or_404(Issue.objects.select_related("category", "location", "reporter"), slug=slug)
    return render(request, "issues/detail.html", {"issue": issue, "timeline": issue.timeline.all()})


@login_required
def report_issue(request):
    if request.method == "POST":
        form = IssueReportForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(reporter=request.user)
            messages.success(request, "Thanks — your report is in and will be verified shortly.")
            return redirect(issue.get_absolute_url())
    else:
        form = IssueReportForm()
    return render(request, "issues/report.html", {"form": form})

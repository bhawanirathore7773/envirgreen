from django.urls import path
from . import views

app_name = "issues"

urlpatterns = [
    path("", views.issue_list, name="list"),
    path("report/", views.report_issue, name="report"),
    path("<slug:slug>/", views.issue_detail, name="detail"),
]

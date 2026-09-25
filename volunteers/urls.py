from django.urls import path
from . import views

app_name = "volunteers"

urlpatterns = [
    path("", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
]

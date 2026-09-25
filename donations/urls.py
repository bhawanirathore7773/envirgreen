from django.urls import path
from . import views

app_name = "donations"

urlpatterns = [
    path("<slug:slug>/", views.donate, name="donate"),
]

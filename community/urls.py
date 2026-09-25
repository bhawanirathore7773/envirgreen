from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("post/", views.create_post, name="create_post"),
    path("post/<int:post_id>/react/", views.react, name="react"),
]

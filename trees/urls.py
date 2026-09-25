from django.urls import path
from . import views

app_name = "trees"

urlpatterns = [
    path("", views.tree_map, name="map"),
    path("plant/", views.plant_tree, name="plant"),
]

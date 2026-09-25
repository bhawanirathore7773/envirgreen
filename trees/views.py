from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import TreePlantationForm
from .models import TreePlantation


def tree_map(request):
    trees = TreePlantation.objects.select_related("location", "planter")
    return render(request, "trees/map.html", {"trees": trees})


@login_required
def plant_tree(request):
    if request.method == "POST":
        form = TreePlantationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(planter=request.user)
            messages.success(request, "Logged — thank you. It'll show as 'Planted' until the team verifies it.")
            return redirect("trees:map")
    else:
        form = TreePlantationForm()
    return render(request, "trees/plant.html", {"form": form})

from django import forms
from core.models import Location
from .models import TreePlantation


class TreePlantationForm(forms.ModelForm):
    city = forms.CharField(max_length=100)
    area = forms.CharField(max_length=150, required=False)

    class Meta:
        model = TreePlantation
        fields = ["species", "count", "photo", "organisation", "planted_on"]
        widgets = {"planted_on": forms.DateInput(attrs={"type": "date"})}

    def save(self, commit=True, planter=None):
        location = Location.objects.create(city=self.cleaned_data["city"], area=self.cleaned_data.get("area", ""))
        tree = super().save(commit=False)
        tree.location = location
        tree.planter = planter
        if commit:
            tree.save()
        return tree

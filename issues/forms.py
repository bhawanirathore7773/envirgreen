from django import forms

from core.models import Location
from .models import Issue


class IssueReportForm(forms.ModelForm):
    city = forms.CharField(max_length=100)
    area = forms.CharField(max_length=150, required=False, label="Area / landmark")

    class Meta:
        model = Issue
        fields = ["title", "category", "description", "photo", "severity", "is_recurring"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def save(self, commit=True, reporter=None):
        location = Location.objects.create(city=self.cleaned_data["city"], area=self.cleaned_data.get("area", ""))
        issue = super().save(commit=False)
        issue.location = location
        issue.reporter = reporter
        if commit:
            issue.save()
        return issue

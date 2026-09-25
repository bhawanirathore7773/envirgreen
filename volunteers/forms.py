from django import forms
from .models import Volunteer


class VolunteerRegistrationForm(forms.ModelForm):
    consent_given = forms.BooleanField(
        required=True, label="I consent to being contacted about volunteering opportunities."
    )

    class Meta:
        model = Volunteer
        fields = ["mobile", "age_group", "skills", "interests", "availability", "emergency_contact", "consent_given"]
        widgets = {"skills": forms.CheckboxSelectMultiple()}

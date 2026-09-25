from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    city = forms.CharField(required=False, max_length=100)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.profile.city = self.cleaned_data.get("city", "")
            user.profile.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["city", "bio", "avatar"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 3, "maxlength": 280})}

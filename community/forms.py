from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["post_type", "text", "image", "campaign"]
        widgets = {"text": forms.Textarea(attrs={"rows": 3})}

from django import forms
from .models import UserPost

# Handles the functionality and basic design of what the post box looks like
class PostForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Post something!",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = UserPost
        exclude = ("user", )
from django import forms
from .models import UserPost
from .models import Post 

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

#This function adds how large the comment box is supposed to be from width to length.
class CommentForm(forms.ModelForm):
    content = forms.CharField(label = "", widget = forms.Textarea(
    attrs = {
        'class':'form-control',
        'placeholder':'Comment here !',
        'rows': 4,
        'cols': 50
    }))
    class Meta: 
        model = Post
        fields = ['content']


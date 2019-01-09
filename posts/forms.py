from django import forms
from .models import Post, PostUpdate


class PostFilterForm(forms.Form):
    page = forms.IntegerField()


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "cover_image")


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostUpdate
        fields = ['content']

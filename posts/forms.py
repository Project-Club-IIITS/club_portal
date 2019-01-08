from django import forms
from .models import Post

class PostFilterForm(forms.Form):
    page = forms.IntegerField()

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title","body","cover_image")
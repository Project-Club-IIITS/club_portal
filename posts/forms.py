from django import forms
from posts.models import *


class PostFilterForm(forms.Form):
    page = forms.IntegerField()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'cover_image')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('start_date','end_date','venue')

from django import forms
from .models import Post, PostUpdate


class PostFilterForm(forms.Form):
    page = forms.IntegerField(required=False)
    events_only = forms.BooleanField(required=False, initial=False)
    polls_only = forms.BooleanField(required=False, initial=False)
    query = forms.CharField(required=False)

    def filter_posts(self, posts):

        if self.is_valid():
            if self.cleaned_data['events_only']:
                posts = posts.exclude(event=None)

            if self.cleaned_data['polls_only']:
                posts = posts.exclude(poll=None)

            if self.cleaned_data['query'] != 'None':
                posts = posts.filter(title__contains=self.cleaned_data['query'])
            #
        return posts


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "cover_image")


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = PostUpdate
        fields = ['content']

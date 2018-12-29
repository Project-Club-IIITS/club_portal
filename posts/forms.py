from django import forms


class PostFilterForm(forms.Form):
    page = forms.IntegerField()



from django import forms

from accounts.models import Calendar


class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['new_password'] != cleaned_data['new_password2']:
            self.add_error('new_password2', 'Both Passwords do not match!')


MONTHS = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)


class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = (
            'title',
        )


class ChooseMonthAndYearForm(forms.Form):
    month = forms.ChoiceField(choices=MONTHS)
    year = forms.ChoiceField(choices=[(x, x) for x in range(1950, 3000)], initial=2019)

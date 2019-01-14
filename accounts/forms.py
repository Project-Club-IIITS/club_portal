from django import forms


class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['new_password'] != cleaned_data['new_password2']:
            self.add_error('new_password2', 'Both Passwords do not match!')

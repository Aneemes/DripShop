# myapp/forms.py
from django import forms
from .models import UserAccount

class CustomSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Retype Password")

    class Meta:
        model = UserAccount

        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'password1',
            'password2',
        )

        field_order = ['email', 'first_name', 'last_name', 'phone', 'address', 'password1', 'password2']


    def signup(self, request, user):
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.save()

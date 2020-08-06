from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Hasło"}))


def validate_password(value):
    if value.islower() or value.isalpha() or value.isdigit() or len(value) <= 7:
        raise ValidationError(
            "Twoje hasło musi zawierać wielką literę, małą literę, cyfrę oraz mieć conajmniej 7 znaków.")


class RegistrationForm(forms.Form):
    password = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'placeholder': "Hasło"}),
                               validators=[validate_password])
    password2 = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'placeholder': "Powtórz hasło"}),
                                validators=[validate_password])
    email = forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={'placeholder': "Email"}))
    name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'placeholder': "Imię"}))
    surname = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'placeholder': "Nazwisko"}))

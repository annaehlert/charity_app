from django import forms
from django.core.exceptions import ValidationError

from main.models import Donation, Category, Institution


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


class DonationForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput
    (attrs={'id': 'quantity'}))
    categories = forms.ModelMultipleChoiceField(
        label="categories",
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all(),
        # to_field_name='name',
    )
    institution = forms.ModelChoiceField(
        label="institution",
        widget=forms.RadioSelect,
        queryset=Institution.objects.all(),
        # to_field_name='name',
    )
    address = forms.CharField(max_length=100, widget=forms.TextInput
    (attrs={'id': 'address'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput
    (attrs={'id': 'phone_number'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput
    (attrs={'id': 'city'}))
    zip_code = forms.CharField(max_length=6, widget=forms.TextInput
    (attrs={'id': 'zip_code'}))
    pick_up_date = forms.DateField(widget=forms.DateInput(attrs={'id': 'pick_up_date'}))
    pick_up_time = forms.TimeField(widget=forms.TimeInput(attrs={'id': 'pick_up_time'}))
    pick_up_comment = forms.CharField(max_length=255, required=False,
                                      widget=forms.Textarea(attrs={'id': 'pick_up_comment'}))

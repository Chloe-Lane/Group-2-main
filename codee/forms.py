from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User



class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birth_month = forms.ChoiceField(choices=[...])  # add your choices here
    birth_day = forms.ChoiceField(choices=[...])
    birth_year = forms.ChoiceField(choices=[...])
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    country = forms.ChoiceField(choices=[...])  # add your countries here
    captcha = CaptchaField()  # Add this line for CAPTCHA



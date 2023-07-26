from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from accounts.models import User


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
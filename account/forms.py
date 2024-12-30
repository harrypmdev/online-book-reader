"""Django forms file for forms utilised in account/views.py.

Forms:
RegisterForm -- a form for user registration on the register page.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    """A form for user registration."""

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        # Ensure multiple users cannot register with the same email.
        # Method written by Trey Hunner -
        # https://stackoverflow.com/questions/52639834/how-to-make-django-form-field-unique.
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

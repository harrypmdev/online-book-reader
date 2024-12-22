"""Django forms file for forms utilised in account/views.py.

Forms:
RegisterForm -- a form for user registration on the register page.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    """A form for user registration."""
    class Meta:
        model = User
        fields = ['username','email','password1','password2']  
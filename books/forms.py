from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book, UserBook

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] 

class ManageForm(forms.ModelForm):
    class Meta:
        model = UserBook
        fields = ['title', 'author']

class URLForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('url',)
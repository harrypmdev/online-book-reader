from django import forms
from .models import Book, UserBook

class ManageForm(forms.ModelForm):
    class Meta:
        model = UserBook
        fields = ['title', 'author']

class URLForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('url',)
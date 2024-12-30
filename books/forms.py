"""Django forms file for forms utilised in books/views.py.

Forms:
ManageForm -- a form for managing the title and author of a UserBook
              on the manage book page.
URLForm -- a form for submitting a URL on the add book page.
"""

from django import forms
from .models import Book, UserBook


class ManageForm(forms.ModelForm):
    """A form for managing the title and author of a UserBook"""

    class Meta:
        model = UserBook
        fields = ["title", "author"]


class URLForm(forms.ModelForm):
    """A form for submitting a URL when adding a book."""

    class Meta:
        model = Book
        fields = ("url",)

"""Django views file that defines views related to user authorisation
and profile management.

Views:
register -- display the register page.
login_view -- display the login page.
logout_view -- log out the user and redirect them to home page.
profile -- display the profile page.
delete_profile -- delete the user's profile.
"""

from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from books.models import Book, UserBook
from . import utility


def register(request):
    """Display the register page.
    Registers user, logs them in and redirects to home page if user
    inputs valid registration data.

    **Context**
    register_form -- an instance of RegisterForm.

    **Template**
    `account/register.html`
    """
    if request.method == "POST":
        poss_redirect = _register_post(request)
        if isinstance(poss_redirect, HttpResponseRedirect):
            return poss_redirect
    register_form = RegisterForm()
    context = {"register_form": register_form}
    return render(
        request,
        "account/register.html",
        context,
    )


def login_view(request):
    """Display the login page.
    Logs in user and redirects to home page if user inputs valid
    login data.

    **Context**
    authentication_form -- an instance of AuthenticationForm.

    **Template**
    `account/login.html`
    """
    if request.method == "POST":
        poss_redirect = _login_view_post(request)
        if isinstance(poss_redirect, HttpResponseRedirect):
            return poss_redirect
    authentication_form = AuthenticationForm()
    context = {"authentication_form": authentication_form}
    return render(
        request,
        "account/login.html",
        context,
    )


def logout_view(request):
    """Log out the user and redirect them to home page."""
    if request.user.is_authenticated:
        utility.add_logged_out_message(request)
        logout(request)
    return redirect("home")


def profile(request):
    """Display the profile page.
    If user is not authenticated, redirects to home page.

    **Context**
    user -- an instance of User. The current user who is viewing the page.
    book_number -- the number of books the current user has on their dashboard.

    **Template**
    `account/profile.html`
    """
    if not request.user.is_authenticated:
        utility.add_authentication_issue_message(request)
        return redirect("home")
    context = {
        "user": request.user,
        "book_number": UserBook.objects.filter(user=request.user.id).count(),
    }
    return render(
        request,
        "account/profile.html",
        context,
    )


def delete_profile(request):
    """Delete the user's profile.
    If user is not logged in, redirects to home page.
    """
    try:
        assert request.user.is_authenticated
        request.user.delete()
        utility.add_account_deleted_message(request)
    except AssertionError:
        utility.add_delete_profile_error_message(request)
    return redirect("home")


def _login_view_post(request):
    # Handle post functionality for the login view.
    # If form is valid, register user with it, log them in and redirect
    # them to home page. Otherwise, inform user registration failed.
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        utility.add_logged_in_message(request)
        return redirect("home")
    utility.add_invalid_credentials_message(request)


def _register_post(request):
    # Handle post functionality for the register view.
    # If form is valid, register user with it, log them in and redirect
    # them to home page. Otherwise, inform user registration failed.
    register_form = RegisterForm(data=request.POST)
    if register_form.is_valid():
        register_form.save()
        utility.add_registered_message(request)
        username = register_form.cleaned_data["username"]
        password = register_form.cleaned_data["password1"]
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("home")
    else:
        utility.add_registration_failed_message(request)

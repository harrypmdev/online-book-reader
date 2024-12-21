from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import RegisterForm
from books.models import Book, UserBook
from . import utility


def register(request):
    if request.method == "POST":
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
            utility.addRegistration_failed_message(request)
    register_form = RegisterForm()
    context = {"register_form": register_form}
    return render(
        request,
        "account/register.html",
        context,
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            utility.add_invalid_credentials_message(request)
        login(request, user)
        utility.add_logged_in_message(request)
        return redirect("home")
    authentication_form = AuthenticationForm()
    context = {"authentication_form": authentication_form}
    return render(
        request,
        "account/login.html",
        context,
    )


def logout_view(request):
    utility.add_logged_out_message(request)
    logout(request)
    return redirect("home")


def profile(request):
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
    try:
        assert request.user.is_authenticated
        request.user.delete()
        utility.add_account_deleted_message(request)
        return redirect("home")
    except AssertionError:
        utility.add_delete_profile_error_message(request)
    return redirect("home")

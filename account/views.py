from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import RegisterForm
from books.models import Book, UserBook

def register(request):
    if request.method == "POST":
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.add_message(
                request, 
                messages.SUCCESS,
                'Account Registered!'
            )
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(
                request, 
                messages.ERROR,
                'Registration unsuccessful! Try another username or password.'
            )
    register_form = RegisterForm()
    context = {"register_form": register_form}
    return render(
        request,
        'account/register.html',
        context,
    )

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(
                request, 
                messages.SUCCESS,
                'Logged in!'
            )
            return redirect('home')
        else:
            messages.add_message(
                request, 
                messages.ERROR,
                'Invalid credentials.'
            )
    authentication_form = AuthenticationForm()
    context = {"authentication_form": authentication_form}
    return render(
        request,
        'account/login.html',
        context,
    )

def logout_view(request):
    messages.add_message(
        request, 
        messages.SUCCESS,
        'Logged out!'
    )
    logout(request)
    return redirect('home')

def profile(request):
    if not request.user.is_authenticated:
        messages.add_message(
            request, 
            messages.ERROR,
            'There was an authentication issue - try clicking "profile" on ' +
            'your navigation bar when logged in.'
        )
        return redirect('home')
    context = {
        "user": request.user,
        "book_number": UserBook.objects.filter(user=request.user.id).count(),
    }
    return render(
        request,
        'account/profile.html',
        context,
    )

def delete_profile(request):
    try:
        assert request.user.is_authenticated
        request.user.delete()
        messages.add_message(
            request, 
            messages.SUCCESS,
            'Your account was successfully deleted.'
        )
        return redirect('home')
    except:
        messages.add_message(
            request, 
            messages.ERROR,
            'There was an authentication issue - try clicking "profile" on ' +
            'your navigation bar when logged in, then clicking "delete profile".'
        )
    return redirect('home')

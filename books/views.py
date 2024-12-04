from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import RegisterForm

# Create your views here.
def about_us(request):
    context = {}
    return render(
        request,
        'books/about_us.html',
        context,
    )

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
            return redirect('about_us')
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
        'books/register.html',
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
            return redirect('about_us')
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
        'books/login.html',
        context,
    )

def logout_view(request):
    messages.add_message(
        request, 
        messages.SUCCESS,
        'Logged out!'
    )
    logout(request)
    return redirect('about_us')
from django.shortcuts import render
from django.contrib import messages
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
    register_form = RegisterForm()
    context = {"register_form": register_form}
    return render(
        request,
        'books/register.html',
        context,
    )
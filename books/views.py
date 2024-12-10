from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import RegisterForm, URLForm
from .models import Book, UserBook

# Create your views here.
def about_us(request):
    context = {}
    return render(
        request,
        'books/about_us.html',
        context,
    )

def home(request):
    context = {}
    link = 'books/home.html'
    if request.user.is_authenticated:
        user_books = UserBook.objects.filter(user=request.user.id)
        context['user_books'] = user_books
        link = 'books/dashboard.html'
    return render(
        request,
        link,
        context,
    )

def add_book(request):
    if request.method == "POST":
        url_form = URLForm(request.POST)
        if url_form.is_valid():
            book_url = url_form.cleaned_data['url']
            try:
                book = Book.objects.get(url=book_url)
            except Book.DoesNotExist:
                book = Book.objects.create(url=book_url)
                book.scan()
                book.save()
            try:
                user_book = UserBook.objects.get(book=book.id, user=request.user.id)
            except UserBook.DoesNotExist:
                user_book = UserBook.objects.create(
                    user=request.user, 
                    book=book,
                    title = book.auto_title,
                    author = book.auto_author
                )
                user_book.pick_color()
                user_book.save()
            return redirect('home')
    url_form = URLForm()
    context = {"form": url_form}
    return render(
        request,
        'books/add_book.html',
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
    return redirect('home')
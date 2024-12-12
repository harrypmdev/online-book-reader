from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import RegisterForm, URLForm, ManageForm
from .models import Book, UserBook, Rating

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
        user_books = UserBook.objects.filter(user=request.user.id).order_by('-last_viewed')
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
            if book_url[len(book_url)-4:len(book_url)] != ".txt":
                messages.add_message(
                    request, 
                    messages.ERROR,
                    'Your URL is not a text file. Please ensure your URL ends with ".txt".'
                )
                return redirect('add_book')
            try:
                book = Book.objects.get(url=book_url)
            except Book.DoesNotExist:
                book = Book.objects.create(url=book_url)
                book.scan()
                book.save()
            try:
                user_book = UserBook.objects.get(book=book.id, user=request.user.id)
                messages.add_message(
                    request, 
                    messages.INFO,
                    'You already had this book in your library. You can update its title and author any time, ' +
                    'by clicking&emsp;<i class="fa-solid fa-pen-to-square"></i>&emsp;below the book you want to edit on the home screen.'
                )
            except UserBook.DoesNotExist:
                user_book = UserBook.objects.create(
                    user=request.user, 
                    book=book,
                    title = book.auto_title,
                    author = book.auto_author
                )
                user_book.pick_color()
                user_book.save()
            return redirect('manage_book', id=user_book.id)
    return render(
        request,
        'books/add_book.html',
        {},
    )

def manage_book(request, id):
    user_book = UserBook.objects.get(id=id, user=request.user)
    book = Book.objects.get(id=user_book.book.id)
    if request.POST:
        if request.POST['rating'] != 0:
            try:
                rating = Rating.objects.get(book=book, user=request.user)
                rating.rating = request.POST['rating']
                rating.save()
            except Rating.DoesNotExist:
                Rating.objects.create(
                    book=book,
                    user=request.user,
                    rating=request.POST['rating'],
                )
        manage_form = ManageForm(data=request.POST)
        if manage_form.is_valid():
            messages.add_message(
                request, 
                messages.SUCCESS,
                'Book saved!'
            )
            user_book.title = manage_form.cleaned_data['title']
            user_book.author = manage_form.cleaned_data['author']
            user_book.save()
            return redirect('home')
    context = {}
    context['rating_count'] = Rating.objects.filter(book=book.id).count()
    context['rated'] = 'false'
    context['average_rating'] = book.average_rating()
    try:
        if Rating.objects.get(book=book.id, user=request.user):
            context['rated'] = 'true'
    except Rating.DoesNotExist:
        context['rated'] = 'false'
    try:
        user_book = UserBook.objects.get(id=id, user=request.user)
        context['book'] = user_book
    except UserBook.DoesNotExist:
        messages.add_message(
            request, 
            messages.ERROR,
            'Authorisation error.'
        )
        return redirect('home')
    context['book'] = user_book
    return render(
        request,
        'books/manage_book.html',
        context,
    )

def delete_book(request, id):
    try:
        user_book = UserBook.objects.get(user=request.user, id=id)
        book = Book.objects.get(id=user_book.book.id)
        if book.total_readers() == 1:
            book.delete()
        user_book.delete()
        messages.add_message(
            request, 
            messages.SUCCESS,
            'Book successfully deleted from library.'
        )
    except Book.DoesNotExist:
        messages.add_message(
            request, 
            messages.ERROR,
            'You are not authorised to delete this book.'
        )
    return redirect('home')
    

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
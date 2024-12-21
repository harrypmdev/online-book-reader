from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from .forms import URLForm, ManageForm
from .models import Book, UserBook, Rating
from . import utility

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
            if not utility.is_text_file(book_url):
                utility.add_not_a_text_file_message(request)
                return redirect('add_book')
            if not utility.is_valid_url(book_url):
                utility.add_invalid_url_message(request)
                return redirect('add_book')
            book = utility.get_book_or_create(book_url)
            user_book = utility.get_user_book_or_create(request, book)
            return redirect('manage_book', id=user_book.id)
    return render(
        request,
        'books/add_book.html',
        {},
    )

def manage_book(request, id):
    user_book = utility.user_book_exists(request, id)
    if not user_book:
        return redirect('home')
    book = Book.objects.get(id=user_book.book.id)
    if request.POST:
        utility.update_rating_if_appropriate(request.POST['rating'], book)
        manage_form = ManageForm(data=request.POST)
        if manage_form.is_valid():
            utility.action_manage_form(request, user_book, manage_form)
            return redirect('home')
    context = {}
    context['rating_count'] = Rating.objects.filter(book=book.id).count()
    context['average_rating'] = book.average_rating()
    context['rated'] = utility.rating_exists(request, book)
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
        utility.add_book_deleted_message(request)
    except UserBook.DoesNotExist:
        utility.add_not_authorised_to_delete_message(request)
    return redirect('home')

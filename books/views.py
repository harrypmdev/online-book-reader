"""Django views file that defines views related to introduction to the
OnlineBookReader site and management of books.

Views:
about_us -- display the about us page.
home -- display the home page.
dashboard -- display the dashboard page.
add_book -- display the add book page.
manage_book - display the manage book page.
delete_book - delete the UserBook matching the given id.
"""

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .forms import URLForm, ManageForm
from .models import Book, UserBook, Rating
from . import utility


def about_us(request):
    """Display the about us page.

    **Template**
    `books/about_us.html`
    """
    return render(
        request,
        "books/about_us.html",
        {},
    )


def home(request):
    """Display the home page.
    Redirects to dashboard if user is authenticated.

    **Template**
    `books/home.html`
    """
    if request.user.is_authenticated:
        return dashboard(request)
    return render(
        request,
        "books/home.html",
        {},
    )


def dashboard(request):
    """Display the dashboard page.

    **Context**
    user_books -- an QuerySet of the user's books, ordered from most recently
                  viewed to least recently viewed.

    **Template**
    `books/dashboard.html`
    """
    user_books = UserBook.objects.filter(user=request.user.id).order_by("-last_viewed")
    return render(request, "books/dashboard.html", {"user_books": user_books})


def add_book(request):
    """Display the add book page.
    Redirects to manage book page if user inputs valid URL.

    **Template**
    `books/add_book.html`
    """
    if request.method == "POST":
        possible_redirect = _add_book_post(request)
        if isinstance(possible_redirect, HttpResponseRedirect):
            return possible_redirect
    return render(
        request,
        "books/add_book.html",
        {},
    )


def manage_book(request, id):
    """Display the manage book page for the given id.
    Redirects to home page if book does not exist for the current user.
    Saves data and redirects to home page if user inputs valid data to
    manage form and submits.

    **Arguments**
    id -- the id for the UserBook in question.

    **Context**
    rating_count -- the number of ratings that exist for this book.
    average_rating -- the average rating for this book.
    rated -- whether the user has already left a rating for this book.
    book -- the UserBook which is being managed.

    **Template**
    `books/manage_book.html
    """
    user_book = utility.user_book_exists(request, id)
    if not user_book:
        return redirect("home")
    book = Book.objects.get(id=user_book.book.id)
    if request.POST:
        poss_redirect = _manage_book_post(request, book, user_book)
        if isinstance(poss_redirect, HttpResponseRedirect):
            return poss_redirect
    context = {}
    context["rating_count"] = Rating.objects.filter(book=book.id).count()
    context["average_rating"] = book.average_rating()
    context["rated"] = utility.rating_exists(request, book)
    context["book"] = user_book
    return render(
        request,
        "books/manage_book.html",
        context,
    )


def delete_book(request, id):
    """Delete the UserBook matching the given id.
     Redirects to home page.
     Adds message to user informing they are not authorised to delete book
     if applicable.

    **Arguments**
     id -- the id for the UserBook in question.
    """
    try:
        user_book = UserBook.objects.get(user=request.user, id=id)
        book = Book.objects.get(id=user_book.book.id)
        if book.total_readers() == 1:
            book.delete()
        user_book.delete()
        utility.add_book_deleted_message(request)
    except UserBook.DoesNotExist:
        utility.add_not_authorised_to_delete_message(request)
    return redirect("home")


def _manage_book_post(request, book, user_book):
    # Handle post functionality for the manage_book view.
    # Update the user's rating if appropriate.
    # Update the book title and author.
    utility.update_rating_if_appropriate(
        request.user, 
        request.POST["rating"], 
        book
    )
    manage_form = ManageForm(data=request.POST)
    if manage_form.is_valid():
        utility.action_manage_form(request, user_book, manage_form)
        return redirect("home")


def _add_book_post(request):
    # Handle post functionality for the add_book view.
    # If given URL is valid, redirects to the manage book page
    # for the given book. If is invalid, displays relevant message.
    url_form = URLForm(request.POST)
    if not url_form.is_valid():
        utility.add_invalid_url_message(request)
        return
    book_url = url_form.cleaned_data["url"]
    if not utility.is_valid_and_txt_url(request, book_url):
        return
    book = utility.get_book_or_create(book_url)
    user_book = utility.get_user_book_or_create(request, book)
    return redirect("manage_book", id=user_book.id)

from django.contrib import messages
from .models import Book, UserBook, Rating


def add_not_a_text_file_message(request):
    messages.add_message(
        request,
        messages.ERROR,
        'Your URL is not a text file. Please ensure your URL ends with ".txt".',
    )


def add_book_in_library_message(request):
    messages.add_message(
        request,
        messages.INFO,
        "You already had this book in your library. You can update its title and author any time, "
        + 'by clicking&emsp;<i class="fa-solid fa-pen-to-square"></i>&emsp;below the book you want to edit on the home screen.',
    )


def add_book_saved_message(request):
    messages.add_message(request, messages.SUCCESS, "Book saved!")


def add_simple_authorisation_error_message(request):
    messages.add_message(request, messages.ERROR, "Authorisation error.")


def add_book_deleted_message(request):
    messages.add_message(
        request, messages.SUCCESS, "Book successfully deleted from library."
    )


def add_not_authorised_to_delete_message(request):
    messages.add_message(
        request, messages.ERROR, "You are not authorised to delete this book."
    )


def get_book_or_create(book_url):
    try:
        return Book.objects.get(url=book_url)
    except Book.DoesNotExist:
        book = Book.objects.create(url=book_url)
        book.scan()
        book.save()
        return book


def get_user_book_or_create(request, book):
    try:
        user_book = UserBook.objects.get(book=book.id, user=request.user.id)
        add_book_in_library_message(request)
    except UserBook.DoesNotExist:
        user_book = UserBook.objects.create(
            user=request.user, book=book, title=book.auto_title, author=book.auto_author
        )
        user_book.pick_color()
        user_book.save()
    return user_book


def update_rating_if_appropriate(request, book):
    if int(request.POST["rating"]) != 0:
        try:
            rating = Rating.objects.get(book=book, user=request.user)
            rating.rating = request.POST["rating"]
            rating.save()
        except Rating.DoesNotExist:
            Rating.objects.create(
                book=book,
                user=request.user,
                rating=request.POST["rating"],
            )


def action_manage_form(request, user_book, manage_form):
    add_book_saved_message(request)
    update_user_book_with_form(user_book, manage_form)


def rating_exists(book, request):
    filter_ratings = Rating.objects.filter(book=book.id, user=request.user)
    return "true" if filter_ratings.exists() else "false"


def update_user_book_with_form(user_book, manage_form):
    user_book.title = manage_form.cleaned_data["title"]
    user_book.author = manage_form.cleaned_data["author"]
    user_book.save()


def user_book_exists(id, request):
    try:
        user_book = UserBook.objects.get(id=id, user=request.user)
        return user_book
    except UserBook.DoesNotExist:
        add_simple_authorisation_error_message(request)
        return False


def is_text_file(book_url):
    return book_url[len(book_url) - 4 : len(book_url)] == ".txt"

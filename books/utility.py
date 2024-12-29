"""A module for simple utility functions utilised in books/views.py.

Public Functions:
add_book_deleted_message -- add message to inform user their book was
                            successfully deleted.
add_not_authorised_to_delete_message -- add message to inform user they are
                                        not authorised to delete the book they
                                        attempted to delete.
add_invalid_url_message -- add message to inform user the URL they entered
                           is invalid.
get_book_or_create -- return the relevant Book for a url if the book with that
                      url already exists. Otherwise, create a new book with
                      that url and return that.
get_user_book_or_create -- return the relevant UserBook for a User and Book if
                           that UserBook already exists. Otherwise, create a
                           new UserBook and return that.
update_rating_if_appropriate -- if a given rating is more than 0, apply the
                                rating to the given book.
action_manage_form -- action a manage_form if it is valid.
rating_exists -- return 'true' if the given user has already rated a book,
                 'false' if not.
user_book_exists -- return the UserBook instance related to the given id
                    if it exists. If it does not exist, return None.
is_valid_and_txt_url -- return True if a given URL links to both a valid
                        destination a text file specifically, False if
                        it does not.
"""

import urllib.request
from django.contrib import messages
from .models import Book, UserBook, Rating


def add_book_deleted_message(request):
    """Add message to inform user their book was successfully deleted.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(
        request, messages.SUCCESS, "Book successfully deleted from library."
    )


def add_not_authorised_to_delete_message(request):
    """Add message to inform user they are not authorised to delete the
    book they attempted to delete.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(
        request, messages.ERROR, "You are not authorised to delete this book."
    )


def add_invalid_url_message(request):
    """Add message to inform user the URL they entered is invalid.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    msg = "This URL is invalid. Check if you typed it correctly or try another version."
    messages.add_message(request, messages.ERROR, msg)


def get_book_or_create(book_url):
    """Return the relevant Book for a url if the book with that url already
    exists. Otherwise, create a new book with that url and return that.

    Arguments:
    book_url: str -- the url for the book which should be either retrieved
                        or created.

    Returns a Book object.
    """
    try:
        return Book.objects.get(url=book_url)
    except Book.DoesNotExist:
        book = Book.objects.create(url=book_url)
        book.scan()
        book.save()
        return book


def get_user_book_or_create(request, book):
    """Return the relevant UserBook for a User and Book if that UserBook
    already exists. Otherwise, create a new UserBook and return that.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    book: Book -- the Book object which, along with the User, is one of two
                  foreign keys that identifies a UserBook.

    Returns a UserBook object.
    """
    try:
        user_book = UserBook.objects.get(book=book.id, user=request.user.id)
        _add_book_in_library_message(request)
    except UserBook.DoesNotExist:
        user_book = UserBook.objects.create(
            user=request.user, book=book, title=book.auto_title, author=book.auto_author
        )
        user_book.pick_color()
        user_book.save()
    return user_book


def update_rating_if_appropriate(user, ratingNum, book):
    """If a given rating is more than 0, apply the rating to the given book.
    Updates a rating if it already exists and creates a new rating if one
    it does not exist already.

    Arguments:
    ratingNum: int -- the rating number in question, from 0 to 10.
    book: Book -- the Book the rating is intended for.
    """
    if int(ratingNum) != 0:
        try:
            rating = Rating.objects.get(book=book, user=user)
            rating.rating = ratingNum
            rating.save()
        except Rating.DoesNotExist:
            Rating.objects.create(
                book=book,
                user=user,
                rating=ratingNum,
            )


def action_manage_form(request, user_book, manage_form):
    """Action a manage_form if it is valid. Update the given user_book with
    the information from the manage_form and add a message to inform the user.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    user_book: UserBook -- the UserBook for which details should be updated.
    manage_form: ManageForm -- the form from which information should be taken
                               and applied to the UserBook instance.
    """
    _add_book_saved_message(request)
    _update_user_book_with_form(user_book, manage_form)


def rating_exists(request, book):
    """Return 'true' if the given user has already rated this book,
    'false' if not.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    book: Book -- the Book for which a rating should be searched.

    Returns a string - either 'true' or 'false'. Returns strings instead of
    a Python Boolean type as this function facilitates the setting of HTML
    attributes which are then read by JS, which uses lower case booleans.
    """
    filter_ratings = Rating.objects.filter(book=book.id, user=request.user)
    return "true" if filter_ratings.exists() else "false"


def user_book_exists(request, id):
    """Return the UserBook instance related to the given id if it exists.
    If it does not exist, return None.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    id: int -- the id for which a UserBook should be retrieved if it exists.

    Returns a UserBook if one is found for the id in question. Otherwise,
    returns None.
    """
    try:
        assert(request.user.is_authenticated)
        user_book = UserBook.objects.get(id=id, user=request.user)
        return user_book
    except (UserBook.DoesNotExist, AssertionError):
        _add_simple_authorisation_error_message(request)


def is_valid_and_txt_url(request, book_url):
    """Check whether a given URL links to both a valid destination and
    a text file specifically. Adds message to user to indicate issue
    with URL if is not both valid and a text file.

    Arguments:
    book_url: str -- the url which should be checked.

    Returns a Boolean, true if the URL is valid, false if not.
    """
    if not _is_text_file(book_url):
        _add_not_a_text_file_message(request)
        return False
    if not _is_valid_url(book_url):
        add_invalid_url_message(request)
        return False
    return True


def _is_text_file(book_url):
    return book_url[len(book_url) - 4 : len(book_url)] == ".txt"


def _is_valid_url(url):
    try:
        urllib.request.urlopen(url)
        return True
    except urllib.error.URLError:
        return False


def _update_user_book_with_form(user_book, manage_form):
    user_book.title = manage_form.cleaned_data["title"]
    user_book.author = manage_form.cleaned_data["author"]
    user_book.save()


def _add_book_in_library_message(request):
    msg = (
        "You already had this book in your library. "
        + "You can update its title and author any time, "
        + 'by clicking edit &emsp;<i class="fa-solid fa-pen-to-square">'
        + "</i>&emsp;below the book you want to edit on the home screen."
    )
    messages.add_message(request, messages.INFO, msg)


def _add_simple_authorisation_error_message(request):
    messages.add_message(request, messages.ERROR, "Authorisation error.")


def _add_not_a_text_file_message(request):
    messages.add_message(
        request,
        messages.ERROR,
        'Your URL is not a text file. Please ensure your URL ends with ".txt".',
    )


def _add_book_saved_message(request):
    messages.add_message(request, messages.SUCCESS, "Book saved!")

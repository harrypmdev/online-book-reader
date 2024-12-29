"""A module for simple utility functions utilised in reader/views.py.

Public Functions:
add_invalid_read_message -- add message to inform user their attempt to
                            read a book with a given id was invalid.
"""

from django.contrib import messages


def add_invalid_read_message(request):
    """Add message to inform user their attempt to read a book with a given
    id was invalid.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    msg = (
        "You are not reading this book. "
        + "Click a book on your dashboard when logged in to access it."
    )
    messages.add_message(request, messages.ERROR, msg)

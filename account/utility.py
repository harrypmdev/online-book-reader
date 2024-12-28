"""A module for simple utility functions utilised in account/views.py.

Public Functions:
add_registered_message -- add message to inform user they have
                           registered successfully.
add_registration_failed_message -- add message to inform user their
                                   registration was unsuccessful.
add_logged_in_message -- add message to inform user they logged in
                         successfully.
add_invalid_credentials_message -- add message to inform user their
                                   credentials are invalid.
add_logged_out_message -- add message to inform user they have logged out.
add_authentication_issue_message -- add message to inform user there was
                                    an authentication issue.
add_account_deleted_message -- add message to inform user their account
                               has been successfully deleted.
add_delete_profile_error_message -- add message to inform user there was
                                    an authentication issue when attempting
                                    to delete their profile.
"""

from django.contrib import messages


def add_registered_message(request):
    """Add message to inform user they have registered successfully.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(request, messages.SUCCESS, "Account Registered!")


def add_registration_failed_message(request):
    """Add message to inform user their registration was unsuccessful.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    msg = ("Registration unsuccessful! Try another username or password. "
            + "You can only register with an email once.")
    messages.add_message(
        request,
        messages.ERROR,
        msg
    )


def add_logged_in_message(request):
    """Add message to inform user they logged in successfully.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(request, messages.SUCCESS, "Logged in!")


def add_invalid_credentials_message(request):
    """Add message to inform user their credentials are invalid.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(request, messages.ERROR, "Invalid credentials.")


def add_logged_out_message(request):
    """Add message to inform user they have logged out.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(request, messages.SUCCESS, "Logged out!")


def add_authentication_issue_message(request):
    """Add message to inform user there was an authentication issue.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(
        request,
        messages.ERROR,
        'There was an authentication issue - try clicking "profile" on '
        + "your navigation bar when logged in.",
    )


def add_account_deleted_message(request):
    """Add message to inform user their account has been successfully deleted.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(
        request, messages.SUCCESS, "Your account was successfully deleted."
    )


def add_delete_profile_error_message(request):
    """Add message to inform user there was an authentication issue when
    attempting to delete their profile.

    Arguments:
    request: HttpRequest -- the request from the view which is directly or
                            indirectly calling this function.
    """
    messages.add_message(
        request,
        messages.ERROR,
        'There was an authentication issue - try clicking "profile" on '
        + 'your navigation bar when logged in, then clicking "delete profile".',
    )

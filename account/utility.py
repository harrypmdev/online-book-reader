from django.contrib import messages


def add_registered_message(request):
    messages.add_message(request, messages.SUCCESS, "Account Registered!")


def add_registration_failed_message(request):
    messages.add_message(
        request,
        messages.ERROR,
        "Registration unsuccessful! Try another username or password.",
    )


def add_logged_in_message(request):
    messages.add_message(request, messages.SUCCESS, "Logged in!")


def add_invalid_credentials_message(request):
    messages.add_message(request, messages.ERROR, "Invalid credentials.")


def add_logged_out_message(request):
    messages.add_message(request, messages.SUCCESS, "Logged out!")


def add_authentication_issue_message(request):
    messages.add_message(
        request,
        messages.ERROR,
        'There was an authentication issue - try clicking "profile" on '
        + "your navigation bar when logged in.",
    )


def add_account_deleted_message(request):
    messages.add_message(
        request, messages.SUCCESS, "Your account was successfully deleted."
    )


def add_delete_profile_error_message(request):
    messages.add_message(
        request,
        messages.ERROR,
        'There was an authentication issue - try clicking "profile" on '
        + 'your navigation bar when logged in, then clicking "delete profile".',
    )

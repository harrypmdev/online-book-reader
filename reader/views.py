"""Django views file that defines views related to the reading of a
given book.

Views:
read -- display the read page.

API Endpoints:
ajax_book_info -- API endpoint for ajax requests from the frontend for book
                  split into lines of a given width.
ajax_update_progress -- API endpoint for ajax requests from the frontend to
                        update the user's progress for a Userbook.
"""

import json
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from books.models import Book, UserBook
from . import utility


def read(request, id):
    """Display the read page.
     Display error message and redirect if there is no UserBook for
     the user with the given id.

    **Arguments**
     id -- the id for the UserBook that is being read.

     **Context**
     progress -- the user's current progress through this book.
     book_id -- the id of the UserBook in question.
     title -- the title of this book.

     **Template**
     `reader/read.html`
    """
    try:
        user_book = UserBook.objects.get(id=id, user=request.user.id)
    except UserBook.DoesNotExist:
        utility.add_invalid_read_message(request)
        return redirect("home")
    user_book.last_viewed = timezone.now()
    user_book.save()
    context = {
        "progress": user_book.progress,
        "book_id": id,
        "title": user_book.title,
    }
    return render(request, "reader/read.html", context)


def ajax_book_info(request):
    """API endpoint for ajax requests from the frontend for book
     split into lines of a given width.

    **JSON Arguments**
     book_id -- the id for the UserBook that is being read.
     num -- the maximum number of characters that should be on one line.

     Returns JSONResponse with a value 'text_list' - either the book in
     question, or an error message if valid information was not POSTed.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        book = Book.objects.get(id=UserBook.objects.get(id=data["book_id"]).book.id)
        return_data = book.return_split_text_list(data["num"])
        return JsonResponse(return_data, safe=False)
    return JsonResponse({"text_list": "Invalid: valid information was not posted."})


def ajax_update_progress(request):
    """API endpoint for ajax requests from the frontend to update the
     user's progress for a Userbook.

    **JSON Arguments**
     book_id -- the id for the UserBook that is being updated.
     progress -- the progress value to which the UserBook should be updated.
     length -- the total length of the book, so percentage progress can be
               calculated.

     Returns JSONResponse with a value 'completion' -- an update on whether the
     attempt to update progress was successful.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            user_book = UserBook.objects.get(id=data["book_id"], user=request.user)
            user_book.progress = data["progress"]
            user_book.update_percent_progress(data["length"])
            user_book.save()
            return JsonResponse({"completion": "Progress updated."})
        except UserBook.DoesNotExist:
            return JsonResponse(
                {"completion": "Invalid: valid information was not posted."}
            )
    return JsonResponse({"completion": "Invalid: valid information was not posted."})

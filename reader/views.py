import json
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from books.models import Book, UserBook


# Create your views here.
def read(request, id):
    user_book = UserBook.objects.get(id=id)
    title = user_book.title
    user_book.last_viewed = timezone.now()
    user_book.save()
    context = {
        "progress": user_book.progress,
        "book_id": id,
        "title": title,
    }
    return render(request, "reader/read.html", context)


def ajax_book_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        book = Book.objects.get(id=UserBook.objects.get(id=data["book_id"]).book.id)
        return_data = book.return_split_text_list(data["num"])
        return JsonResponse(return_data, safe=False)
    return JsonResponse({"text_list": "Invalid: valid information was not posted."})


def ajax_update_progress(request):
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

import json
from django.shortcuts import render
from django.http import JsonResponse
from books.models import Book, UserBook

# Create your views here.
def read(request, id):
    title = UserBook.objects.get(id=id).title
    current_page = 1
    context = {
        "current_page": current_page,
        "book_id": id,
        "title": title,
    }
    return render(request, 'reader/read.html', context)

def ajax_book_info(request):
    print("request received")
    if request.method == "POST":
        data = json.loads(request.body)
        book = Book.objects.get(id=UserBook.objects.get(id=data['book_id']).book.id)
        print("RECEIVED NUM: " + str(data['num']))
        return_data = book.return_split_text_list(data['num'])
        for line in return_data[:200]:
            print(str(len(line)))
        return JsonResponse(return_data, safe=False)
    return JsonResponse({'text_list': 'Invalid: valid information was not posted.'})
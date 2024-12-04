from django.shortcuts import render

# Create your views here.
def about_us(request):
    context = {}
    return render(
        request,
        'books/about_us.html',
        context,
    )

def register(request):
    context = {}
    return render(
        request,
        'books/register.html',
        context,
    )
from . import views
from django.urls import path

urlpatterns = [
    path('ajaxbookinfo/', views.ajax_book_info, name="ajax"),
    path('<int:id>/', views.read, name='read'),
]
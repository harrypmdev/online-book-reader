from django.contrib import admin
from .models import Book, UserBook, Rating

# Register your models here.
admin.site.register(Rating)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
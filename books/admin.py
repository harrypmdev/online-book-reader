from django.contrib import admin
from .models import Book, UserBook

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
from django.contrib import admin
from .models import Category, Author, Book, BookLoan, BookRating, BookComment

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(BookLoan)
admin.site.register(BookRating)
admin.site.register(BookComment)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    raw_id_fields = ('category', 'author')
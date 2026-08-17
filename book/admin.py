from django.contrib import admin

from .models import Book, UserBook

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display_links = []
    list_display = [
        'title',
        'slug',
        'author',
        'published_date',
        'annotation',
    ]
    list_filter = ['genre']
    prepopulated_fields = {
        'slug': ('title', 'author')
    }

@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display_links = []
    list_display = [
        'user',
        'book',
        'rate',
        'status',
        'notes',
        'review'
    ]
    list_filter = ['status', 'rate']
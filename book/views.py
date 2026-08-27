from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag

from .models import Book

def book_list(request: HttpRequest):

    genre_slug = request.GET.get('genre')

    books = Book.objects.all()
    genres = Book.genre.all()
    if genre_slug:
        books = books.filter(genre__slug=genre_slug)

    books = books.prefetch_related('genre')

    paginator = Paginator(books, 24)
    page = request.GET.get('page')
    books_only = request.GET.get('books_only')

    try:
        books = paginator.page(page) #type: ignore

    except PageNotAnInteger:
        books = paginator.page(1)

    except EmptyPage:
        if books_only:
            return HttpResponse('')

        books = paginator.page(paginator.num_pages)

    if books_only:
        return render(
            request,
            'books/list.html',
            {
                'section': 'books',
                'books': books,
                'genres': genres
            }
        )

    return render(
                request,
                'books/book_list.html',
                {
                    'section': 'books',
                    'books': books,
                    'genres': genres
                }
            )

def filter_by_genre(request: HttpRequest, genre_slug):

    genre = Book.genre.filter(slug=genre_slug)
    books = Book.objects.filter(genre__in = genre).all()

    return books

def book_detail(request: HttpRequest, slug):

    book = get_object_or_404(Book, slug=slug)

    return render(
        request,
        'books/book/detail.html',
        {
            'book': book
        }
    )
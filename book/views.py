from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Book

def book_list(request: HttpRequest):

    books = Book.objects.all()
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
                'books': books
            }
        )

    return render(
                request,
                'books/book_list.html',
                {
                    'section': 'books',
                    'books': books
                }
            )

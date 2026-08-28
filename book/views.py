from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from taggit.models import Tag

from .models import Book, UserBook

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
    rate = UserBook.objects.values_list('rate', flat=True)[0]

    return render(
        request,
        'books/book/detail.html',
        {
            'book': book,
            'rate': rate
        }
    )

@login_required
@require_POST
def book_rate(request: HttpRequest):
    print('called')

    id = request.POST.get('id')
    rate = request.POST.get('rate')

    print(id)
    print(rate)

    if id and rate:

        try:
            book = Book.objects.get(id=id)

            try:
                user_book, is_created = UserBook.objects.update_or_create(defaults= {
                    'user': request.user,
                    'book': book,
                    'rate': rate,
                }
                )

                print(user_book)

                return JsonResponse({'status': 'ok'})

            except:
                return JsonResponse({'status': 'error'})

        except (Book.DoesNotExist, Book.MultipleObjectsReturned):
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})
            
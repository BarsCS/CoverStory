from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings

import redis

from .models import Book, UserBook

r = redis.Redis(host = settings.REDIS_HOST, port = settings.REDIS_PORT, db = settings.REDIS_DB, decode_responses=True)

def book_list(request: HttpRequest):

    genre_slug = request.GET.get('genre')

    books = Book.objects.all().order_by('-views')
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
    rate = None
    
    redis_key = f'book:{book.pk}:viewers'

    if request.user.is_authenticated:
        user_book = UserBook.objects.filter(
                user = request.user,
                book = book
            ).first()

        rate = user_book.rate if user_book else None

        user_identifier = f'user:{request.user.pk}'

    else:

        if not request.session.session_key:
            request.session.create()

        user_identifier = f'session:{request.session.session_key}'

    pipe = r.pipeline()

    pipe.sadd(redis_key, user_identifier)

    pipe.scard(redis_key)

    results = pipe.execute()

    is_new = results[0]
    total_views = results[1]

    if is_new:
        r.zincrby('book:ranking', 1, book.pk)

    return render(
        request,
        'books/book/detail.html',
        {
            'book': book,
            'rate': rate,
            'total_views': total_views
        }
    )

@login_required
@require_POST
def book_rate(request: HttpRequest):

    book_id = request.POST.get('book_id')

    try:
        rate = int(request.POST.get('rate', ''))
    except ValueError:
        return JsonResponse({'status': 'error'}, status = 400)

    if rate not in UserBook.Rating.values:
        return JsonResponse({'status': 'error'}, status = 400)

    if book_id and rate:

        try:
            book = Book.objects.get(id=book_id)

            user_book, is_created = UserBook.objects.update_or_create(
                user = request.user,
                book = book,
                defaults={'rate': rate}
            )

            return JsonResponse({'status': 'ok'})

        except (Book.DoesNotExist, Book.MultipleObjectsReturned):
            return JsonResponse({'status': 'error'}, status = 400)

    return JsonResponse({'status': 'error'}, status = 400)
        
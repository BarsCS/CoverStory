from venv import create

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator

def get_default_bookshelf():
    bookshelf, _ = UserBookshelf.objects.get_or_create(name="Загальна")
    return bookshelf.pk

class Book(models.Model):

    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.CharField(max_length=60)
    published_date = models.DateField()
    genre = TaggableManager(blank=True)
    annotation = models.TextField(max_length=4000)
    cover = models.ImageField(upload_to='covers/', default='no_cover.png', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='user_bookmarks', blank=True)

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('book:detail', args=[self.slug])


class UserBookshelf(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=4000, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookshelves')

    def __str__(self):
        return f'Bookshelf {self.name} of {self.user.username}'
    

class UserBook(models.Model):

    class Rating(models.IntegerChoices):
        TERRIBLE = 1, 'Terrible'
        POOR = 2, 'Poor'
        AVERAGE = 3, 'Average'
        VERY_GOOD = 4, 'Very Good'
        EXCELLENT = 5, 'Excellent'
    
    class Status(models.TextChoices):
        WANT_TO_READ = 'WTR', 'Want to Read'
        READING = 'READING', 'Reading'
        FINISHED = 'FINISHED', 'Finished'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_users')
    bookshelf = models.ForeignKey(
        UserBookshelf,
        on_delete=models.SET_DEFAULT,
        default=get_default_bookshelf,
        related_name='user_books'
    )

    rate = models.PositiveSmallIntegerField(choices=Rating.choices, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.WANT_TO_READ)

    notes = models.TextField(max_length=4000, blank=True)
    review = models.TextField(max_length=4000, blank=True)

    pages_read = models.PositiveIntegerField(default=0)
    started_at = models.DateField(null=True, blank=True)
    finished_at = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book')
        ]

    def __str__(self):
        return f'{self.book.title} - {self.user.username} - {self.rate}'

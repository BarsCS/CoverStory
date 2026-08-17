from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager

class Book(models.Model):

    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100)
    author = models.CharField(max_length=60)
    published_date = models.DateField()
    genre = TaggableManager(blank=True)
    annotation = models.TextField(max_length=4000)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    bookmarks = models.ManyToManyField(User, related_name='user_bookmarks')

    def __str__(self):
        return f'{self.title} by {self.author}'

class UserBook(models.Model):

    RATING_CHOICES = [
        (1, 'Terrible'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]
    
    class Status(models.TextChoices):
        WANT_TO_READ = 'WTR', 'Want to Read'
        READING = 'READING', 'Reading'
        FINISHED = 'FINISHED', 'Finished'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_users')

    rate = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5, blank=True)
    status = models.CharField(choices=Status, default=Status.WANT_TO_READ)
    notes = models.TextField(max_length=4000, blank=True)

    pages_read = models.IntegerField(default=0)
    started_at = models.DateField(null=True, blank=True)
    finished_at = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.TextField(max_length=4000)


    def __str__(self):
        return f'{self.book.title} - {self.user.username}'

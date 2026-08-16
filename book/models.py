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

    def __str__(self):
        return f'{self.title} by {self.author}'


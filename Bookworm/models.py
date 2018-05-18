from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Author(models.Model):
    author_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.author_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    title = models.CharField(max_length=128)
    ISBN10 = models.CharField(unique=True, max_length=10)
    cover = models.ImageField(upload_to='static/book_images', blank=True)
    genres = models.ManyToManyField(Genre)
    authors = models.ManyToManyField(Author)
    bookslug = models.SlugField(unique=True)
    rating = models.FloatField()

    def save(self, *args, **kwargs):
        self.bookslug = slugify(self.title) + "-" + slugify(self.ISBN10)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000, blank=True)
    picture = models.ImageField(upload_to='static/profile_images', blank=True)
    read = models.ManyToManyField(Book, blank=True, related_name='has_read')
    userslug = models.SlugField(unique=True)
    to_read = models.ManyToManyField(Book, blank=True, related_name='to_read')

    def save(self, *args, **kwargs):
        self.userslug = slugify(self.user_name)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_name.username

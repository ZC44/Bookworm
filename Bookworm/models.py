from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Author(models.Model):
    author_name = models.CharField(max_length=128,unique=True)

    def __str__(self):
        return self.author_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=128, unique=True)
    genreslug = models.SlugField(unique=True)

    def save(self,*args,**kwargs):
        self.genreslug = slugify(self.genre_name)
        super(Genre,self).save(*args,**kwargs)

    def __str__(self):
        return self.genre_name

class Book(models.Model):
    title = models.CharField(max_length=128)
    ISBN10 = models.CharField(unique=True,max_length=10)
    cover = models.ImageField(upload_to='book_images', blank=True)
    genres = models.ManyToManyField(Genre)
    authors = models.ManyToManyField(Author)
    bookslug = models.SlugField(unique=True)
    rating = models.FloatField()
    rated_by = models.ManyToManyField(User)

    def save(self,*args,**kwargs):
        self.bookslug = slugify(self.title)
        super(Book,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user_name = models.OneToOneField(User)
    bio = models.CharField(max_length=1000,blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    to_read = models.ManyToManyField(Book, blank=True, related_name = 'has_read')
    userslug = models.SlugField(unique=True)
    has_read = models.ManyToManyField(Book, related_name = 'to_read')


    def save(self, *args, **kwargs):
        self.userslug = slugify(self.user_name)
        super(UserProfile,self).save(*args,**kwargs)

    def __str__(self):
        return self.user_name.username

    def __unicode__(self):
        return self.user_name.username

# @receiver(post_save,sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#     instance.profile.save()

class Rate(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(UserProfile)
    rating = models.IntegerField(blank=True)

    def __str__(self):
        return self.book
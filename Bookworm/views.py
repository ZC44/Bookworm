import json

from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.db.models import Avg
from Bookworm.models import *
from Bookworm.forms import *

# Create your views here.

def home(request):
    popular = Book.objects.order_by('-rating')[:5]
    try:
        user = request.user
        user_profile = UserProfile.objects.get(user_name=user)
        toRead = user_profile.objects.get('to_read')
        read = user_profile.objects.get('has_read')
        rec = Book.objects.all().exclude(toRead).exclude(read)[:5]
        recommendations = reversed(rec)
    except:
        recommendations = Book.objects.order_by('-rating')[:5]
    context_dict = {'popular': popular, 'recommendations': recommendations}
    response = render(request, 'Bookworm/home.html', context=context_dict)
    return response

def show_book(request, bslug):
    context_dict = {}
    context_dict['display_rate'] = False
    context_dict['read'] = False
    context_dict['toread'] = False
    try:
        book = Book.objects.all().get(bookslug=bslug)
        context_dict['book'] = book
        context_dict['authors'] = book.authors.all()
        context_dict['genres'] = book.genres.all()
        context_dict['bslug'] = bslug
        context_dict['rating'] = book.rating

        if request.user.is_authenticated():
            ratings = book.rated_by.all()
            user = request.user
            user_profile = UserProfile.objects.get(user_name=user)
            if user not in ratings:
                context_dict['display_rate'] = True

            if book in user_profile.has_read.all():
                context_dict['read'] = True

            if book in user_profile.to_read.all():
                context_dict['toread'] = True



        return render(request, 'Bookworm/book.html', context=context_dict)
    except:
        context_dict['book'] = None
        context_dict['authors'] = None
        context_dict['genres'] = None
        context_dict['rating'] = None
        return render(request,'Bookworm/404.html')

def show_genre(request):
    context_dict = {}
    context_dict['genres'] = Genre.objects.order_by('genre_name')
    context_dict['bookgenres'] = Book.objects.values_list('bookslug','title','genres',)
    return render(request, 'Bookworm/genres.html',context=context_dict)

def userpage(request,uslug):
    context_dict = {}

    try:
        if request.method == 'POST':

            try:
                user = request.user
                user_profile = UserProfile.objects.get(user_name=user)
                context_dict['user'] = user
                context_dict['to_read'] = user_profile.to_read.all()
                context_dict['has_read'] = user_profile.has_read.all()
            except:
                context_dict['user'] = None
            return render(request, 'Bookworm/userprofile.html',context=context_dict)
    except:
        return render(request,'Bookworm/404.html')

def recommendations(request,uslug):
    context_dict = {}
    return render(request, 'Bookworm/recommendations.html',context=context_dict)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                django_login(request, user)
                return home(request)
            else:
                return HttpResponse("Your Bookworm account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return home(request)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user_name = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                registered = True
            profile.save()
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'Bookworm/register.html',{'user_form': user_form,'profile_form': profile_form,
                                                    'registered': registered})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def sorry(request):
    return render(request, 'Bookworm/404.html')

def rating(request):
    return render(request, 'Bookworm/rating.html')



def search_results(request):
    context = {}
    search = request.GET.get('search')

    # based on value of radio button
    search_type = request.GET['searchtype']
    if search_type == 'ISBN10':
        context['results'] = Book.objects.filter(ISBN10__icontains=search)
    elif search_type == 'Title':
        context['results'] = Book.objects.filter(title__icontains=search)
    elif search_type == 'Author':
        context['results'] = Book.objects.filter(authors__author_name__icontains=search).distinct()

    return render(request, 'Bookworm/searchresults.html', context = context)




def rate(request,bslug):
    context = RequestContext(request)

    if request.method == 'POST':
        book = Book.objects.get(bookslug=bslug)
        rating = int(request.POST.get('ratescore'))

        ratingno = book.rated_by.count()
        book.rating = (book.rating * ratingno + rating)
        ratingno += 1
        book.rating = book.rating / ratingno



        user = request.user
        user_profile = UserProfile.objects.get(user_name=user)

        book.rated_by.add(user)

        book.save()
    return show_book(request,bslug)


def has_read(request, bslug):
    context = RequestContext(request)

    if request.method == 'POST':
        book = Book.objects.get(bookslug=bslug)

        user = request.user
        user_profile = UserProfile.objects.get(user_name=user)

        user_profile.has_read.add(book)

    return show_book(request, bslug)


def to_read(request,bslug):
    context = RequestContext(request)

    if request.method == 'POST':
        book = Book.objects.get(bookslug=bslug)

        user = request.user
        user_profile = UserProfile.objects.get(user_name=user)

        user_profile.to_read.add(book)

    return show_book(request, bslug)
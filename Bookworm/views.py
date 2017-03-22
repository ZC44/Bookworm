from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db.models import Avg
from Bookworm.models import *
from Bookworm.forms import *

# Create your views here.

def home(request):
    rating_list = Rate.objects.all()
    #if rating_list is None:
    popular = Book.objects.order_by('?')[:5]
    # else:
    #     for book in rating_list:
    #
    #         b = {'title': , 'authors': ,'rating': }
    try:
        toRead = UserProfile.objects.get('toRead')
        read = Rate.objects.filter(user=UserProfile.userslug)
        rec = Book.objects.all().exclude(toRead).exclude(read)[:5]
        recommendations = rec
    except:
        recommendations = Book.objects.order_by('?')[:5]
    context_dict = {'popular': popular, 'recommendations': recommendations}
    response = render(request, 'Bookworm/home.html', context=context_dict)
    return response

def show_book(request, bslug):
    context_dict = {}
    try:
        book = Book.objects.all().get(bookslug=bslug)
        context_dict['book'] = book
        context_dict['authors'] = book.authors.all()
        context_dict['genres'] = book.genres.all()
        try:
            context_dict['rating'] = Rate.objects.filter(book=book).aggregate(Avg('rating'))
        except:
            context_dict['rating'] = None
        return render(request, 'Bookworm/book.html', context=context_dict)
    except:
        context_dict['book'] = None
        context_dict['authors'] = None
        context_dict['genres'] = None
        context_dict['rating'] = None
        return HttpResponse('Bookworm/404.html')

def show_genre(request):
    context_dict = {}
    context_dict['genres'] = Genre.objects.order_by('genre_name')
    context_dict['bookgenres'] = Book.objects.values_list('bookslug','title','genres',)
    return render(request, 'Bookworm/genres.html',context=context_dict)

def search_results(request):
    context_dict = {}
    return render(request, 'Bookworm/searchresults.html',context=context_dict)

def userpage(request,uslug):
    context_dict = {}
    try:
        user = UserProfile.objects.get(userslug=uslug)
        context_dict['user'] = user
        context_dict['toRead'] = user.toRead.all()
        context_dict['read'] = Rate.objects.filter(user=user)
    except:
        context_dict['user'] = None
    return render(request, 'Bookworm/userprofile.html',context=context_dict)

def recommendations(request,uslug):
    context_dict = {}
    return render(request, 'Bookworm/recommendations.html',context=context_dict)

def base(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('base'))
            else:
                return HttpResponse("Your Bookworm account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'Bookworm/base.html', {})

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
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                registered = True
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
"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from Bookworm import views

urlpatterns = (
    url(r'^$', views.home, name='home'),
    url(r'^book/(?P<bslug>[\w\-]+)/$', views.show_book, name='show_book'),
    url(r'^genres/$', views.show_genre, name='show_genre'),
    url(r'^search_results/$', views.search_results, name='search_results'),
    url(r'^user/(?P<uslug>[\w\-]+)/$', views.userpage, name='user'),
    url(r'^user/(?P<uslug>[\w\-]+)/recommendations/$', views.recommendations, name='recommendations'),
    url(r'^base/$', views.base, name='base'),
    url(r'^register/$',views.register, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^404/$', views.sorry, name='404')
)
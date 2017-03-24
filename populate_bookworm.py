import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'Project.settings')

import django
django.setup()
from Bookworm.models import Book, Genre,bookwithGenres,bookswithauthors,Author

def populate():

	book1 = {"title": "5555cd555",
			"authors" : ("gggg","hhhghgg"),
			"genres":("action","thehell2") ,
			"ISBN10" : "15010"
			}
	

	#math3 = [{"title": "leniar","ISBN10":"131111"}]
		
	books =[book1]



	#for bok in books:
	b = add_book(book1["title"],book1["authors"],book1["genres"],book1["ISBN10"])
		
		
	for b in Book.objects.all():
		for g, a in zip(bookwithGenres.objects.filter(book =b.title), bookswithaurhors.objects.filter(book =b.title)):
				print("- {0} - {1} - {2}".format(str(b.title), str(g.genre),str(a.author)))

def add_book(title,authors,Gens,ISBN10):
	b,created = Book.objects.get_or_create(title = title,ISBN10 = ISBN10)
	ISBN10 = ISBN10
	print b
	
	b.save()
	for g in Gens :
		add_bookwithGenres(g,title)
	for a in authors:
		add_bookswithauthors(title,a)
	return b

def add_Gen(genre_name):
	g, created = Genre.objects.get_or_create(genre_name =genre_name)
	g.save()
	return g
def add_author(Author_name):
	a,created = Author.objects.get_or_create(author_name =Author_name)
	a.save()
	return a


def	add_bookwithGenres(genre,book):
	add_Gen(genre)
	bg, created = bookwithGenres.objects.get_or_create(genre = genre,book=book)
	bg.save()
	return 
	

def add_bookswithauthors(Book,Author):
	add_author(Author)
	ba,created = bookswithauthors.objects.get_or_create(author=Author)
	ba.book = Book
	ba.save()
	return ba

if __name__ == '__main__':
	print("Starting bookworm population script...")
	populate()
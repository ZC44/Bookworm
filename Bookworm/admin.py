from django.contrib import admin
from Bookworm.models import *

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'userslug': ('user_name',)}


class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'bookslug': ('title',)}


admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(UserProfile, UserProfileAdmin)

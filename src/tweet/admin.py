from django.contrib import admin
from .models import Tweet


class TweetAdmin(admin.ModelAdmin):
    list_display = ['author', 'content']
    search_fields = ['author', 'content']
    

admin.site.register(Tweet, TweetAdmin)



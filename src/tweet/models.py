from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import validate_comma_separated_integer_list, validate_integer
from django.db import models
from django.db.models.signals import post_save


class CustomField(models.CharField):
    widget = models.CharField(max_length=120, verbose_name="CUSTOM")
    
    def __str__(self):
        return "Custom field"


class TweetManager(models.Manager):
    def retweet(self, user, content, parent_tweet):
        new_tweet = self.model(
            parent=parent_tweet,
            author=user,
            content=content,
            # content=parent_tweet.content
        )
        new_tweet.save()
        return new_tweet


class Tweet(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField(max_length=200, verbose_name='Tweet Content')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = TweetManager()
    
    class Meta:
        ordering = ['-timestamp']
    
    # print(dir(validators))
    def __str__(self):
        return f'tweet with id: {self.id}'
    
    def is_retweeted(self):
        if self.parent:
            return True
        return False


from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfileManager(models.Manager):
    def all(self):
        qs = self.get_queryset().all()
        if self.instance:
            qs = qs.exclude(user=self.instance)
        return qs
    
    def toggle_follow(self, current_user, toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=current_user)
        if toggle_user in user_profile.following.all():
            user_profile.following.remove(toggle_user)
            added = False
        else:
            user_profile.following.add(toggle_user)
            added = True
        return added
        
    def is_following(self, current_user, followed_user):
        user_profile, created = UserProfile.objects.get_or_create(user=current_user)
        if followed_user in user_profile.following.all():
            return True
        return False
        

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    user_img = models.ImageField(verbose_name='Image', blank=True, upload_to='profiles')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    
    objects = UserProfileManager()
    
    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)


# we do that to automatically create new profile user..
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    print(instance)
    print(sender)
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)
    else:
        print(f'{instance} is already exist')


post_save.connect(post_save_user_receiver, User)



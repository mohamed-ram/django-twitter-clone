from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import UserProfile


def user_profile(request, user):
    profile = UserProfile.objects.get(user__username=user)
    following = UserProfile.objects.is_following(request.user, profile.user)
    context = {'profile': profile, 'following': following}
    print(following)
    return render(request, 'userprofile/profile.html', context)


# user toggle follow in CBV.
class UserFollow(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
            
            # userprofile, exist = UserProfile.objects.get_or_create(user=request.user)
            # if toggle_user in userprofile.following.all():
            #     userprofile.following.remove(toggle_user)
            # else:
            #     userprofile.following.add(toggle_user)
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# user toggle follow in FBV
def user_follow(request, username):
    toggle_user = get_object_or_404(User, username__iexact=username)
    if request.user.is_authenticated:
        userprofile, exist = UserProfile.objects.get_or_create(user=request.user)
        if toggle_user in userprofile.following.all():
            userprofile.following.remove(toggle_user)
        else:
            userprofile.following.add(toggle_user)
    
    # return redirect("profile:user_profile", user=toggle_user)
    # return redirect(url, user=toggle_user)
    # print(request.META)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms.utils import ErrorList
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import RetweetForm, TweetForm
from .models import Tweet
from django.views.generic import CreateView, ListView, DetailView, UpdateView
import datetime
from django import forms




def home_page(request):
    tweets = Tweet.objects.all()
    return render(request, 'tweet/home_page.html', {'tweets': tweets})


# def tweet_list(request):
#     tweets = Tweet.objects.all().order_by('-timestamp')
#     return render(request, 'tweet/tweet_list.html', {'tweets': tweets})


# def tweet_detail(request, tweet_id):
#     tweet = get_object_or_404(Tweet, id=tweet_id)
#     print(tweet)
#     return render(request, 'tweet/tweet_detail.html', {'tweet': tweet})


# Generic CBV.
class TweetList(ListView):
    model = Tweet
    template_name = 'tweet/tweet_list.html'
    context_object_name = 'tweets'
    
    def get_queryset(self, *args, **kwargs):
        super().get_queryset(*args, **kwargs)
        tweets = Tweet.objects.all()
        query = self.request.GET.get('q')
        if query:
            tweets = tweets.filter(Q(content__icontains=query) | Q(author__username__icontains=query))
       
        return tweets
    
    def get_context_data(self, *args, **kwargs):
        print(self)
        context = super(TweetList, self).get_context_data(*args, **kwargs)
        context['published'] = True
        context["now"] = datetime.datetime.now()
        context['form'] = TweetForm()
        context['retweet_form'] = RetweetForm()
        return context


class TweetDetail(DetailView):
    model = Tweet
    template_name = 'tweet/tweet_detail.html'
    context_object_name = 'tweet'
    
    @property
    def get_model(self):
        return self.model
    
    def get_object(self, *args, **kwargs):
        pk = self.kwargs['tweet_id']
        return Tweet.objects.get(id=pk)
    
    def get_context_data(self, **kwargs):
        context = super(TweetDetail, self).get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        context['now'] = datetime.datetime.now()
        return context
    

# print("List View:", dir(DetailView))

class CreateTweet(CreateView):
    template_name = 'tweet/create_tweet.html'
    # model = Tweet
    # fields = ['content']
    # or
    form_class = TweetForm
    success_url = '/tweets'
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
            return super(CreateTweet, self).form_valid(form)
    
    # def form_valid(self, form):
    #     if not form.instance.published:
    #         form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["must check box.."])
    #         return self.form_invalid(form)
    #
    #     if self.request.user.is_authenticated:
    #         form.instance.author = self.request.user
    #         return super(CreateTweet, self).form_valid(form)
    #     else:
    #         form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["user must be authenticated.."])
    #         return self.form_invalid(form)


class TweetUpdate(LoginRequiredMixin, UpdateView):
    model = Tweet
    fields = ['content']
    template_name = "tweet/update_tweet.html"
    success_url = '/tweets'
    

class Retweet(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated:
            new_tweet = Tweet.objects.retweet(request.user, self.content, tweet)
            # print(new_tweet.is_retweeted())
            return redirect('tweet:tweets')
        

    
    
    




from django.urls import path
from . import views

app_name = 'tweet'

urlpatterns = [
    path('', views.home_page, name="home"),
    # path('tweets', views.tweet_list, name='tweets'),
    path('tweets/', views.TweetList.as_view(), name='tweets'),
    # path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    path('tweet/<int:tweet_id>/', views.TweetDetail.as_view(), name='tweet_detail'),
    path('tweet/create/', views.CreateTweet.as_view(), name='tweet_create'),
    path('tweet/<pk>/retweet/', views.Retweet.as_view(), name='retweet'),
    path('tweet/<int:pk>/update/', views.TweetUpdate.as_view(), name='tweet_update'),
]



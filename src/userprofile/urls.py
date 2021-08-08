from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('<str:user>', views.user_profile, name='user_profile'),
    # toggle user follow => CBV
    path('<str:username>/follow', views.UserFollow.as_view(), name='follow'),
    # toggle user follow => FBV
    # path('<str:username>/follow', views.user_follow, name='follow'),
]


from django.urls import path, re_path
from .views import *
from .views import register
from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Correct import
from . import views

urlpatterns = [
    path('add_friend/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('save_profile/<int:user_id>/', views.save_profile, name='save_profile'),
    path('saved_profiles/', views.view_saved_profiles, name='saved_profiles'),
    path('', TweetListView.as_view(), name='list_view'),
    path('<int:pk>/',  TweetDetailView.as_view(), name='detail_view'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='tweets/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.user_login, name='home'),  # Home or custom login view
]
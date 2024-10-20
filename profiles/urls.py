from django.urls import path
from . import views
from .views import accept_friend_request, decline_friend_request

urlpatterns = [
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline-friend-request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('accept-friend-request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('decline-friend-request/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
    path('notifications/', views.notifications, name='notifications')
]
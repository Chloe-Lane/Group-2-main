"""
URL configuration for codee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from profiles.views import send_friend_request, accept_friend_request, decline_friend_request, user_profile
from tweets.views import user_login

# Import View

# Import View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('tweet/', include('tweets.urls')),
    path('page/<str:username>/', page_view, name='page_view'),
    path('logout/', custom_logout, name='logout'),
    path('captcha/', include('captcha.urls')),
    path('generate_captcha/', generate_captcha, name='generate_captcha'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('send-reset-code/', send_reset_code, name='send_reset_code'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('send-verification-code/', send_verification_code, name='send_verification_code'),
    path('verify-code/', verify_code, name='verify_code'),
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline-friend-request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('profiles/', include('profiles.urls')),
    path('', include('tweets.urls')),  # Include URLs from the tweets app
    path('login/', LoginView.as_view(template_name='tweets/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.user_login, name='home'),
    path('page/<str:username>/album.html', views.album_view, name='album'),
    path('page/<str:username>/album/<int:album_id>/', views.album_view, name='album'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

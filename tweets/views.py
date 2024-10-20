from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Tweet
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Friend, SavedProfile
from django.contrib.auth import authenticate, login, logout  # Correct imports
from django.shortcuts import render, redirect
from django.http import HttpResponse

@login_required
def add_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    friend_list, created = Friend.objects.get_or_create(user=request.user)
    friend_list.friends.add(friend)
    return redirect('friends_list')

@login_required
def remove_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    friend_list = Friend.objects.get(user=request.user)
    friend_list.friends.remove(friend)
    return redirect('friends_list')

@login_required
def friends_list(request):
    friends = Friend.objects.filter(user=request.user).first()
    return render(request, 'tweets/friends_list.html', {'friends': friends})

@login_required
def save_profile(request, user_id):
    saved_user = get_object_or_404(User, id=user_id)
    SavedProfile.objects.create(user=request.user, saved_user=saved_user)
    return redirect('saved_profiles')

@login_required
def view_saved_profiles(request):
    saved_profiles = SavedProfile.objects.filter(user=request.user)
    return render(request, 'tweets/saved_profiles.html', {'saved_profiles': saved_profiles})

# Create your views here.
def tweet_detail_view(request, pk=None):
    obj = Tweet.objects.get(pk=pk)
    print(obj)
    context = {
        'object': obj,
    }
    return render(request, 'tweets/detail_view.html', {})


def tweet_list_view(request):
    qs = Tweet.objects.all()
    print(qs)
    context = {
        'query': qs,
    }
    return render(request, 'tweets/list_view.html', {})




class TweetListView(ListView):
    queryset = Tweet.objects.all()
    template_name = 'tweets/list_view.html'




class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()
    template_name = 'tweets/detail_view.html'

    def get_object(self, queryset=Tweet.objects.all()):
        print(self.kwargs)
        pk=self.kwargs.get('pk')
        print(pk)
        return Tweet.object.get(id=pk)

def home(request):
    return render(request, 'auth/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # If everything is fine, create a new user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('home')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Set session expiry if "Remember Me" is not checked
            if not remember_me:
                request.session.set_expiry(0)  # Session expires on browser close

            return redirect('home')  # Redirect to homepage or dashboard

        return render(request, 'tweets/login.html', {'error': 'Invalid credentials'})

    return render(request, 'tweets/login.html')
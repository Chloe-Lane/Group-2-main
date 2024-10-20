from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from .models import FriendRequest, Profile

def notifications(request):
    if request.user.is_authenticated:
        friend_requests = FriendRequest.objects.filter(to_user=request.user)
        print(friend_requests)  # Check what friend requests are fetched
        return render(request, 'homep/notifications.html', {'friend_requests': friend_requests})
    else:
        print("User is not authenticated.")
        return redirect('login')  # Adjust as necessary

def send_friend_request(request, user_id):
    if request.method == 'POST':
        username = request.POST.get('friend_username')
        to_user = get_object_or_404(User, username=username)  # Change to lookup by username
        from_user = request.user

        if from_user != to_user:
            friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
            if created:
                messages.success(request, f'Friend request sent to {to_user.username}')
            else:
                messages.info(request, 'Friend request already sent')
        else:
            messages.error(request, "You cannot send a friend request to yourself.")

    return redirect('user_profile', user_id=user_id)

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        from_user_profile = Profile.objects.get(user=friend_request.from_user)
        to_user_profile = Profile.objects.get(user=request.user)
        from_user_profile.friends.add(to_user_profile.user)  # Adjusted to add User instance
        to_user_profile.friends.add(from_user_profile.user)
        friend_request.delete()
        messages.success(request, 'Friend request accepted')
    else:
        messages.error(request, 'You cannot accept this friend request.')
    return redirect('home')

def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        messages.info(request, 'Friend request declined')
    else:
        messages.error(request, 'You cannot decline this friend request.')
    return redirect('home')

def friends_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    friends = profile.friends.all()  # Get all friends of the logged-in user
    return render(request, 'homep/friends_list.html', {'friends': friends})

def profile_view(request):
    user = request.user
    return render(request, 'homep/page.html', {'user': user})

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'homep/profile_list.html', {'profiles': profiles})

def profile(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    return render(request, 'homep/profile.html', {'profile': profile})


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'homep/user_profile.html', {'user': user})

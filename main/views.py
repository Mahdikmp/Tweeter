from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Tweet, Comment
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import TweetForm, RegisterForm, ProfileEditForm, PassChangeForm, ProfileImageForm
from .forms import TweetEditForm, CommentForm, UserEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q





def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST, None)
        if request.method == 'POST':
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                return redirect('home')
                messages.info(request, 'Your tweet was posted successfully')
        tweets = Tweet.objects.all().order_by('-created')
        context = {'tweets': tweets, 'form': form}
        return render(request, 'home.html', context)
    else:  
        tweets = Tweet.objects.all().order_by('-created')
        context = {'tweets': tweets}
        return render(request, 'home.html', context)



def profiles_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
    else:
        messages.info(request, ('To see the profiles, You have to login !'))
        return redirect('home')
    
    context = {'profiles': profiles}
    return render(request, 'profiles.html', context)



def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk)
        context = {'profile': profile, 'tweets': tweets}

        if request.method == 'POST':
            currentUserProfile = request.user.profile
            action = request.POST['following']
            if action == 'follow':
                currentUserProfile.follows.add(profile)
            elif action == 'unfollow':
                currentUserProfile.follows.remove(profile)

        return render(request, 'profile.html', context)
    else:
        messages.info(request, ('To see the profiles, You have to login !'))
        return redirect('home')
    


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged In successfully')
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong! Try again.')
            return redirect('login')
    else:
        return render(request, 'login.html')



def logout_user(request):

    logout(request)
    messages.info(request, 'You are logged out successfully')
    return redirect('home')



def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.info(request, 'Your account has been created')
            return redirect('home')

    context = {'form': form}
    return render(request, 'register.html', context)



def editProfile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UserEditForm(request.POST or None, instance = request.user)
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your porfile has been updated')
                return redirect('home')
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            context = {'user_form': user_form, 'profile_form': profile_form}
            return render(request, 'editprofile.html', context)
    else:
        messages.info(request, 'You must login first')
        return redirect('home')
    


def passwordChange(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PassChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user) #stay logged in
                messages.info(request, 'Your password has been changed')
                return redirect('home')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('password_change')
        else:
            form = PassChangeForm(request.user)
            context = {'form': form}
            return render(request, 'passwordch.html', context)
    else:
        messages.info(request, 'You must login first')
        return redirect('home')
    


def profileImageUpdate(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your profile picture has been updated')
            return redirect('home')
    else:
        form = ProfileImageForm(instance=profile)

    context = {'form': form}
    return render(request, 'profile_image.html', context)



# Could do it with ajax
def like(request, tweet_id):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=tweet_id)
        if tweet.likes.filter(id=request.user.id).exists():
            tweet.likes.remove(request.user)
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            tweet.likes.add(request.user)
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')



def tweetShow(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    tweetComments = tweet.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.tweet = tweet
                comment.save()
                
                messages.success(request, 'Your comment was posted')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'The comment can not be empty!')
                return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'You must be logged in')
            return redirect(request.META.get('HTTP_REFERER', 'home'))    
    else:
        form = CommentForm()
        context = {'tweet': tweet, 'comments': tweetComments, 'form': form}
        return render(request, 'tweet.html', context)
    


def tweetDelete(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)

    if request.user.is_authenticated:
        if tweet.user != request.user:
            messages.error(request, 'This is not your tweet')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            if request.method == 'POST':
                tweet.delete()
                messages.success(request, 'Your tweet was deleted')
                return redirect('profile', request.user.id)
        return render(request, 'tweet_delete.html', {'tweet': tweet})
    else:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    


def tweetEdit(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    elif tweet.user != request.user:
        messages.error(request, 'This is not your tweet')
        return redirect('home')
    else:
        if request.method == 'POST':
            form = TweetEditForm(request.POST, instance=tweet)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your tweet was edited')
                return redirect('profile', request.user.id)
        else:
            form = TweetEditForm(instance=tweet)
            return render(request, 'tweet_edit.html', {'form': form})



def follow(request, user_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    else:
        user_to_follow = get_object_or_404(User, id=user_id)
        if request.user == user_to_follow:
            messages.error(request, 'You are already following yourself')
            return redirect('profiles_list')
        else:
            request.user.profile.follows.add(user_to_follow.profile)
            next_page = request.META.get('HTTP_REFERER', 'profiles_list')
            return redirect(next_page)



def unFollow(request, user_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in')
        return redirect('home')
    else:
        user_to_unfollow = get_object_or_404(User, id=user_id)
        if request.user == user_to_unfollow:
            messages.error(request, 'You can not unfollow yourself')
            return redirect('home')
        else:
            request.user.profile.follows.remove(user_to_unfollow.profile)
            next_page = request.META.get('HTTP_REFERER', 'profiles_list')
            return redirect(next_page)



def userFollowers(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'followers.html', context)



def userFollowings(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'followings.html', context)



def userSearch(request):
    query = request.GET.get('q')
    if query:
        query = query.strip()
    else:
        query = ''

    
    profiles = Profile.objects.all()

    if query:
        profiles = profiles.filter(Q(user__username__icontains = query) | Q(bio__icontains=query)).distinct()
    
    context = {'profiles': profiles, 'query': query, 'count': profiles.count()}
    return render(request, 'user_search.html', context)
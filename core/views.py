from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import profile, Post, LikePost, FollowersCount
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from itertools import chain
import random
# Create your views here.
@login_required(login_url='signin')
def index(request):        
    user_object = User.objects.get(username = request.user.username)
    user_profile = profile.objects.get(user = user_object)

    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower = user_profile)

    for users in user_following:
        user_following_list.append(users)

    for usernames in user_following_list:
        user_object = User.objects.get(username = usernames)
        user_profile = profile.objects.get(user = user_object)
        feed_lists = Post.objects.filter(user = user_profile)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))
    
    post = Post.objects.all()

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username = user.user)
        user_following_all.append(user_list)

    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username = request.user.username)
    final_suggestion_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.id)
    
    for ids in username_profile:
        profile_lists = profile.objects.filter(id_user = ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    context = {
        'user_profile':user_profile,
        'post': feed_list,
        'suggestions_username_profile_list':suggestions_username_profile_list[:4]
    }
    return render(request, 'index.html', context)

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        # Fetch the associated profile for the authenticated user
        # user_profile = request.user # Assuming that the profile is associated with the User model
        the_user = profile.objects.get(user = request.user)
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=the_user, image=image, caption=caption)
        new_post.save()
        messages.info(request, 'done')
        return redirect('/')
    else:
        return redirect('/')

def search(request):
    if request.method == "POST":
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_list = profile.objects.filter(id_user = ids)
            username_profile_list.append(profile_list)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'username_profile_list':username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id = post_id, username = username).first()
    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        # Access the specific post instance and update the no_of_likes field
        post.no_of_likes =+ 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes =+ 1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def setting(request):
    user_profile = profile.objects.get(user = request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:

            image = user_profile.profileimg

            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:

            image = request.FILES.get('image')

            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect('index')
    context  = {
        'user_profile' : user_profile
    }
    return render(request, 'setting.html', context)

@login_required(login_url='signin')
def userProfile(request, pk):
    user_object = User.objects.get( username = pk )
    
    user_profile = profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user = user_profile)
    user_posts_lenght = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower = follower, user=user).first():
        button_text = 'following'
    else :
        button_text = 'follow'


    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts, 
        'user_posts_lenght' : user_posts_lenght,
        'button_text' : button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        if FollowersCount.objects.filter(follower = follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/userProfile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/userProfile/' + user)

    else:
        return redirect('/')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email= email).exists():
                messages.info(request, 'this email has already been used')
                return redirect('signup')
            elif User.objects.filter(username= username).exists():
                messages.info(request, 'username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)  
                user.save()

                # log user in and direct to settings page
                user_login = auth.authenticate(username= username, password = password )
                auth.login(request, user_login)
                #  creating profile object for the new user
                user_model = User.objects.get(username= username)
                new_profile = profile.objects.create(user= user_model, id_user = user_model.id )
                new_profile.save()
                return redirect('setting')
        else:
            messages.info(request,  'Passwords dont match, PLease Try Again')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username= username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Name or password')
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
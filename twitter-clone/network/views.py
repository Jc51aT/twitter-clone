import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone,dateformat
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Post_Likes, User_Following

  
def index(request):
    posting = Post()

    if request.method == "POST":
        posting.text = request.POST["post-text"]
        posting.date_time = timezone.now()
        posting.num_likes = 0
        posting.author = request.user
        posting.save()
        return HttpResponseRedirect(reverse("index"))

    
    return render(request, "network/index.html",{
        "Posts": Post.objects.all(),
    })

@csrf_exempt
@login_required
def update_post(request, post_id):

    post = Post.objects.get(author=request.user, pk=post_id)

    if request.method == 'PUT':
        data = json.loads(request.body)
        post.text = data["text"]
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def follow_user(request):

    data = json.loads(request.body)

    if request.method == 'PUT':
        follow_user = User_Following()
        follow_user.user_id = request.user
        f_user = User.objects.get(pk=data["following_user"])
        follow_user.following_user_id = f_user
        follow_user.save()
        return HttpResponse(status=204)
    if request.method == 'DELETE':
        follow_user = User_Following.objects.get(user_id = request.user.id, following_user_id= data["following_user"])
        follow_user.delete()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@login_required
def following(request):
    users_following         =  [e.following_user_id for e in  User_Following.objects.filter(user_id = request.user.id)] 
    users_following_posts   = Post.objects.filter(author__in=users_following)
    

    return render(request, "network/following.html",{
        "Posts": users_following_posts,
    })


@login_required
def profile(request, username=None):
    
    # if the user requesting the page is different from the users profile page
    if username != request.user.username:

        user          = User.objects.get(username=username)
        followers     = list(User_Following.objects.filter(following_user_id= user.id))
        filter_followers    = filter(lambda u_f: u_f.user_id == request.user, followers)
        num_following = len(User_Following.objects.filter(user_id = user.id))
        num_followers = len( User_Following.objects.filter(following_user_id= user.id))
        user_posts    = Post.objects.filter(author= user)
        user_name     = user.username
        user_id       = user.id
        is_follower   = list(filter_followers)[0].user_id == request.user
    else:

        num_following = len(User_Following.objects.filter(user_id = request.user.id))
        followers     = list(User_Following.objects.filter(following_user_id= request.user.id))
        num_followers = len( followers )
        user_posts    = Post.objects.filter(author= request.user)
        user_name     = request.user.username
        user_id       = request.user.id
        is_follower   = False

    return render(request, "network/profile.html", {
        "num_following": num_following,
        "isFollower"   : is_follower,
        "num_followers": num_followers,
        "user_posts"   : user_posts,
        "user_name"    : user_name,
        "user_id"      : user_id,
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

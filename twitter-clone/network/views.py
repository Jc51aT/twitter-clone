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

@login_required
def following(request):
    users_following         =  [e.following_user_id for e in  User_Following.objects.filter(user_id = request.user.id)] 
    users_following_posts   = Post.objects.filter(author__in=users_following)
    

    return render(request, "network/following.html",{
        "Posts": users_following_posts,
    })


@login_required
def profile(request, username=None):

    if username is not None:
        user = User.objects.get(username=username)
        num_following = len(User_Following.objects.filter(user_id = user.id))
        num_followers = len( User_Following.objects.filter(following_user_id= user.id))
        user_posts    = Post.objects.filter(author= user)
        user_name     = user.username
    else:
        num_following = len(User_Following.objects.filter(user_id = request.user.id))
        num_followers = len( User_Following.objects.filter(following_user_id= request.user.id))
        user_posts    = Post.objects.filter(author= request.user)
        user_name     = request.user.username

    return render(request, "network/profile.html", {
        "num_following": num_following,
        "num_followers": num_followers,
        "user_posts"   : user_posts,
        "user_name"    : user_name,
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

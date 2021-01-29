import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone,dateformat
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .models import User, Post, Post_Likes, User_Following

  
def index(request):
    

    if request.method == "POST":
        posting = Post()
        posting.text = request.POST["post-text"]
        posting.date_time = timezone.now()
        posting.num_likes = 0
        posting.author = request.user
        posting.save()
        return HttpResponseRedirect(reverse("index"))

    posts               = Post.objects.all()
    user_liked_posts    = []
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        user_likes          = Post_Likes.objects.filter(user_liked=request.user).select_related('post_id')
        user_liked_posts    = [post.post_id for post in user_likes]
    
    return render(request, "network/index.html",{
        "Posts": posts,
        "Posts_liked": user_liked_posts,
        "page_obj": page_obj
    })

@csrf_exempt
@login_required
def like_post(request, post_id):

    post = Post.objects.get(pk=post_id)

    if request.method == "PUT":
        newLike = Post_Likes(post_id=post, user_liked=request.user)
        post.num_likes += 1
        newLike.save()
        post.save()
        return HttpResponse(status=204)
    elif request.method == "DELETE":
        like = Post_Likes.objects.get(post_id=post, user_liked=request.user)
        like.delete()
        post.num_likes -= 1
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT or DELETE request required."
        }, status=400)


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
        follow_user = User_Following.objects.get(user_id = request.user, following_user_id= data["following_user"])
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
    paginator = Paginator(users_following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html",{
        "Posts": users_following_posts,
        "page_obj": page_obj
    })


@login_required
def profile(request, username=None):
    user_liked_posts = []
    # if the user requesting the page is different from the users profile page
    if username != request.user.username:

        user          = User.objects.get(username=username)
        try:
            followers     = User_Following.objects.get(user_id = request.user, following_user_id= user.id)
            is_follower   = True
            user_likes  = Post_Likes.objects.filter(user_liked=request.user).select_related('post_id')
            user_liked_posts = [post.post_id for post in user_likes]
        except User_Following.DoesNotExist:
            print(User_Following.DoesNotExist)
            is_follower   = False
        except Post_Likes.DoesNotExist:
            print(Post_Likes.DoesNotExist)

        
        num_following = len(User_Following.objects.filter(user_id = user.id))
        num_followers = len( User_Following.objects.filter(following_user_id= user.id))
        user_posts    = Post.objects.filter(author= user)
        user_name     = user.username
        user_id       = user.id
        
    else:

        num_following = len(User_Following.objects.filter(user_id = request.user.id))
        followers     = list(User_Following.objects.filter(following_user_id= request.user.id))
        num_followers = len( followers )
        user_posts    = Post.objects.filter(author= request.user)
        user_name     = request.user.username
        user_id       = request.user.id
        is_follower   = False
    
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "num_following": num_following,
        "isFollower"   : is_follower,
        "num_followers": num_followers,
        "user_posts"   : user_posts,
        "user_name"    : user_name,
        "user_id"      : user_id,
        "Posts_liked": user_liked_posts,
        "page_obj": page_obj
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

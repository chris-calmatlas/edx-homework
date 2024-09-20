import math, json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from .models import User, Post

# Forms
class PostForm(forms.Form):
    content=forms.CharField(
        widget=forms.Textarea()
    )

# views
def index(request):
    return render(request, "network/index.html")


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

@login_required
def newPost(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(
                content=form.cleaned_data['content'],
                owner=request.user
            )

            post.save()

    return redirect("allPosts")

@login_required
def like(request, postId):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=postId)
        except ObjectDoesNotExist:
            raise PermissionDenied
        
        # Check if this user likes this post
        liked = False
        userLikes = post.likes.filter(pk=request.user.id)
        if userLikes:
            liked = True

        # If already liked remove
        if liked:
            try:
                post.likes.remove(request.user)
            except Exception as e:
                print(e)
        else:
            try:
                post.likes.add(request.user)
            except Exception as e:
                print(e)
        
        # Save whatever change we made
        try:
            post.save()
            liked = not liked
        except Exception as e:
            print(e)
        # Toggle like by adding or deleting this user to the post likes
        return JsonResponse({"liked": liked})
    
@login_required
def follow(request, userId):
    if request.method == "POST":
        try:
            target = User.objects.get(pk=userId)
        except ObjectDoesNotExist as e:
            raise PermissionDenied
        
        # Check if this user likes this post
        followed = False
        userFollows = target.followers.filter(pk=request.user.id)
        if userFollows:
            followed = True

        # If already followed remove
        if followed:
            try:
                target.followers.remove(request.user)
            except Exception as e:
                print(e)
        else:
            try:
                target.followers.add(request.user)
            except Exception as e:
                print(e)
        
        # Save whatever change we made
        try:
            target.save()
            followed = not followed
        except Exception as e:
            print(e)
        # Toggle like by adding or deleting this user to the post likes
        return JsonResponse({"following": followed})

@login_required
def following(request):
    # Get all the posts
    allPosts = Post.objects.filter(owner__in=request.user.following.all()).all()
    allPostCount = allPosts.count()
    pageCount = math.floor(allPostCount / 10)
    print(pageCount)

    # Setup the start and end posts for the page
    currentPage = max(int(request.GET.get('page', 1)),1)
    startPost = (currentPage - 1) * 10
    endPost = currentPage * 10

    context = {
        "posts": allPosts.order_by("-createdOn")[startPost:endPost],
        "pageCount": pageCount,
        "currentPage": currentPage
    }

    return render(request, "network/following.html", context)

def allPosts(request):
    # Get all the posts
    allPosts = Post.objects.all()
    allPostCount = allPosts.count()
    pageCount = math.floor(allPostCount / 10)

    # Setup the start and end posts for the page
    currentPage = max(int(request.GET.get('page', 1)),1)
    startPost = (currentPage - 1) * 10
    endPost = currentPage * 10

    context = {
        "postForm": PostForm(),
        "posts": allPosts.order_by("-createdOn")[startPost:endPost],
        "pageCount": pageCount,
        "currentPage": currentPage
    }

    return render(request, "network/allPosts.html", context)

@login_required
def profile(request, userId):
    # Get the target user for the profile page
    try:
        target = User.objects.get(pk=userId)
    except Exception as e:
        print(e)
        return redirect("allPosts")
    
    # Get all posts
    allPosts = Post.objects.filter(owner=target)
    allPostCount = allPosts.all().count()
    pageCount = math.floor(allPostCount / 10)

    # Setup the start and end posts for the page
    currentPage = max(int(request.GET.get('page', 1)),1)
    startPost = (currentPage - 1) * 10
    endPost = currentPage * 10

    context = {
        "target": target,
        "posts": allPosts.order_by("-createdOn")[startPost:endPost],
        "pageCount": pageCount,
        "currentPage": currentPage
    }
    return render(request, "network/userProfile.html", context)

@login_required
def editPost(request,postId):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=postId)
        except ObjectDoesNotExist:
            raise PermissionDenied
        
        if post.owner != request.user:
            raise PermissionDenied
        
        form = PostForm(json.loads(request.body))

        if form.is_valid():
            post.content = form.cleaned_data['content']
            try:
                post.save()
            except Exception as e:
                print(e)
                return JsonResponse({ "success": "false" })
            return JsonResponse({ "success": "true" })
        
    return JsonResponse({ "success": "false" })
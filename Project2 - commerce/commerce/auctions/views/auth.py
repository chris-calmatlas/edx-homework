from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from auctions.models import User

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("active")
        else:
            return render(request, "auctions/auth/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("active")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/auth/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/auth/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("active")
    else:
        return render(request, "auctions/auth/register.html")


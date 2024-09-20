
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("posts", views.allPosts, name="allPosts"), 
    path("newPost", views.newPost, name="newPost"),
    path("following", views.following, name="following"),

    path("profile/<str:userId>", views.profile, name="profile"),
    path("profile/<str:userId>/follow", views.follow, name="follow"),

    path("posts/<str:postId>/like", views.like, name="like"),
    path("posts/<str:postId>/edit", views.editPost, name="editPost")
    
]

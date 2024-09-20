from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="following")

class Post(models.Model):
    content = models.TextField(max_length=600, default="")
    owner = models.ForeignKey("User", null=True, on_delete=models.CASCADE, related_name="posts")
    createdOn = models.DateTimeField(auto_now_add=True)
    modifiedOn = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField("User", related_name="liked")
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("random", views.randomEntry, name="random"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("wiki/<str:entry>", views.entry, name="entry")
]

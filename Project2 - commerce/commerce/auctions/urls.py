from django.urls import path

from .views import *

urlpatterns = [
    path("", search.active, name="active"),
    path("closed", search.closed, name="closed"),
    path("category/<str:category>", search.category, name="listingByCategory"),
    path("categories", search.categories, name="categories"),
    path("watchlist", search.watchlist, name="watchlist"),

    path("login", auth.login_view, name="login"),
    path("logout", auth.logout_view, name="logout"),
    path("register", auth.register, name="register"),

    path("listing/create", listing.create, name="createListing"),
    path("listing/<str:listingId>", listing.get, name="getListing"),
    path("listing/delete/<str:listingId>", listing.delete, name="deleteListing"),
    path("listing/close/<str:listingId>", listing.close, name="closeListing"),

    path("comment/create/<str:listingId>", comment.create, name="createComment"),
    
    path("bid/create/<str:listingId>", bid.create, name="createBid"),

    path("watchlist/toggle/<str:listingId>", watchlist.toggle, name="toggleWatchlist")
]

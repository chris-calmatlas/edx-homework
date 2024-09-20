from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db import IntegrityError

from auctions.models import Listing, Watchlist
from auctions.forms import Checkbox

def toggle(request, listingId):
    # Authenticated only
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        #Get the listing to add or remove
        try:
            listing = Listing.objects.get(pk=listingId)
        except ObjectDoesNotExist:
            raise PermissionDenied
        
        # get or create a watchlist for the user.
        try:
            watchlist = Watchlist.objects.get(user=request.user)
        except ObjectDoesNotExist:
            watchlist = Watchlist(
                user=request.user
            )
            try:
                watchlist.save()
            except IntegrityError:
                request.session['msg'] = f"Problem adding {listing} to your watchlist"
                return redirect("getListing", listingId)
                    
        form = Checkbox(request.POST)

        if form.is_valid():
            print(request.POST)
            if form.cleaned_data['checked']:
                try:
                    watchlist.listings.remove(listing)
                    request.session['msg'] = f"Removed {listing} from your watchlist"
                except:
                    request.session['msg'] = f"Problem removing {listing} from your watchlist"
            else:
                # Add the list to the watchlist.
                try:
                    watchlist.listings.add(listing)
                    request.session['msg'] = f"Added {listing} to your watchlist"
                except:
                    request.session['msg'] = f"Problem adding {listing} to your watchlist"
        return redirect("getListing", listingId)
    # Not a post
    raise PermissionDenied
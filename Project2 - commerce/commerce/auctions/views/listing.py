from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError

from auctions.models import Listing, Category, Comment
from auctions.forms import NewListing, NewBid, ConfirmForm, CommentForm, Checkbox

def create(request):
    # Authenticated only
    if not request.user.is_authenticated:
        return redirect("login")
    
    # Data to include in the template
    data = {
        "newListingForm": NewListing()
    }

    # Clear error messages passed through the session
    if 'msg' in request.session:
        data['msg'] = request.session['msg']
        del request.session['msg']

    # Create a new listing
    if request.method == "POST":
        form = NewListing(request.POST)
        
        if form.is_valid():
            # Validate selected category.
            try:
                category=Category.objects.get(title=form.cleaned_data['category'])
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                category=form.cleaned_data['category']

            listing = Listing(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                startingAmount=form.cleaned_data['startingBid'],
                imageUrl=form.cleaned_data['imageUrl'],
                category=category,
                user=request.user
            )
            try:
                listing.save()
                request.session['msg'] = f"{listing} added"
                return redirect("getListing", listing.id)
            except IntegrityError:
                # Reload the create page with an error
                data['msg'] = f"There was a problem saving your listing."
                data['newListingForm'] = form
                return render(request, "auctions/listing/create.html", data)
        else:
            # The form is invalid reload the page
            # form.errors generates validation errors
            form.errors
            data['newListingForm'] = form
            return render(request, "auctions/listing/create.html", data)
    # Not a POST. render the page
    return render(request, "auctions/listing/create.html", data)

def get(request, listingId):
    # Get the listing from the db
    try:
        listing = Listing.objects.get(pk=listingId)
    except ObjectDoesNotExist:
        redirect("index")

    # Gather additional info to pass
    userIsOwner = False
    userIsWinner = False
    onWatchlist = False
    if request.user.is_authenticated:
        if listing.user == request.user:
            userIsOwner = True
        if listing.winningBid:
            if listing.winningBid.user == request.user:
                userIsWinner = True
        try:
            watchlist = listing.watchlist_set.filter(user=request.user)
            if watchlist:
                onWatchlist = True
        except Exception as error:
            print(error)

    # Data to include in the template
    data = {
        "listing": listing,
        "watchlistForm": Checkbox({"checked": onWatchlist}),
        "bidForm": NewBid(),
        "userIsOwner": userIsOwner,
        "userIsWinner": userIsWinner,
        "onWatchList": onWatchlist,
        "commentForm": CommentForm(),
        "comments": Comment.objects.filter(listing=listingId),
    }

    # Clear error messages passed through the session
    if 'msg' in request.session:
        data['msg'] = request.session['msg']
        del request.session['msg']

    # Render the page
    return render(request, "auctions/listing/get.html", data)

def delete(request, listingId):
    # Authenticated only
    if not request.user.is_authenticated:
        return redirect("login")

    # Get the listing from the db
    try:
        listing = Listing.objects.get(pk=listingId)
    except ObjectDoesNotExist:
        redirect("index")

    # Data to include in the template
    data = {
        "listing": listing,
        "ConfirmForm": ConfirmForm()
    }

    if listing.user == request.user:
        if request.method == "POST":
            form = ConfirmForm(request.POST)
            # Validate confirmation checkbox
            if form.is_valid():
                if form.cleaned_data['Confirm']:
                    try:
                        listing.delete()
                        request.session['msg'] = f"{listing} deleted"
                        return redirect("active")
                    except:
                        request.session['msg'] = f"There was a problem deleting {listing}"
                        return redirect("getListing", listingId)
        # not a post
        return render(request, "auctions/listing/delete.html", data)
    else:
        # the signed in user is not the owner
        raise PermissionDenied

def close(request, listingId):
    # Authenticated only
    if not request.user.is_authenticated:
        return redirect("login")

    # Get the listing from the db
    try:
        listing = Listing.objects.get(pk=listingId)
    except ObjectDoesNotExist:
        redirect("index")

    # Data to include in the template
    data = {
        "listing": listing,
        "ConfirmForm": ConfirmForm()
    }

    if listing.user == request.user:
        if request.method == "POST":
            form = ConfirmForm(request.POST)
            # Validate confirmation checkbox
            if form.is_valid():
                if form.cleaned_data['Confirm']:
                    try:
                        listing.isActive = False
                        listing.save()
                        request.session['msg'] = f"{listing} closed"
                        return redirect("getListing", listingId)
                    except:
                        request.session['msg'] = f"There was a problem closing {listing}"
                        return redirect("getListing", listingId)
        # not a post
        return render(request, "auctions/listing/close.html", data)
    else:
        # the signed in user is not the owner
        raise PermissionDenied


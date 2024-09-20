from django.db import IntegrityError
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from auctions.models import Listing, Bid
from auctions.forms import NewBid

def create(request, listingId):
    # Authenticated only
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form = NewBid(request.POST)
        if form.is_valid():
            # Get the currently winning bid
            try:
                oldBid = Bid.objects.filter(listing=listingId).get(isHighest=True)
            except ObjectDoesNotExist:
                oldBid = None
            
            # get the listing
            try:
                listing=Listing.objects.get(pk=listingId)
            except ObjectDoesNotExist:
                raise PermissionDenied
            
            # Determining winning amount 
            newBidAmount = form.cleaned_data['bidAmount']
            if oldBid:
                amountToBeat = oldBid.amount
            else:
                amountToBeat = listing.startingAmount

            # Validate that new bid is higher
            if newBidAmount > amountToBeat:
                newBidIsHigher = True
            else:
                newBidIsHigher = False
                                   
            # Place the bid
            if newBidIsHigher:
                # Update the winning bid fields
                if oldBid:
                    oldBid.isHighest = False
                newBid = Bid(
                    amount=newBidAmount,
                    listing=listing,
                    user=request.user,
                    isHighest = True
                )
                listing.winningBid = newBid

                # Update the db
                try:
                    if oldBid:
                        oldBid.save()
                    newBid.save()
                    listing.save()
                    return redirect("getListing", listingId)
                except IntegrityError:
                    request.session['msg'] = f"There was a problem saving your bid"
                    return redirect("getListing", listingId)
            else:
                #newBid is lower
                request.session['msg'] = f"Bids must be greater than ${amountToBeat}."
                return redirect("getListing", listingId)
    # Not a POST. redirect to the listing
    return redirect("getListing", listingId)
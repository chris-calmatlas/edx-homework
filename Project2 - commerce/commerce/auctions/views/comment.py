from django.db import IntegrityError
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from auctions.models import Listing, Comment
from auctions.forms import CommentForm

def create(request, listingId):
    # Authenticated only
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            # Post the comment
            try:
                comment = Comment(
                    content=content,
                    user=request.user,
                    listing=Listing.objects.get(pk=listingId)
                )
                comment.save()
                return redirect("getListing", listingId)
            except IntegrityError:
                request.session['msg'] = f"There was a problem saving your comment"
                return redirect("getListing", listingId)
        else:
            form.errors
            return redirect("getListing", listingId)
    # Not a post
    raise PermissionDenied

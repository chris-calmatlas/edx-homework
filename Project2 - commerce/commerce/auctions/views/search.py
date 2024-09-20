from django.shortcuts import render
from auctions.models import Listing, Category, Watchlist

def active(request):
    data = {
        "listings": Listing.objects.filter(isActive=True)
    }
    
    if 'msg' in request.session:
        data['msg'] = request.session['msg']
        del request.session['msg']

    return render(request, "auctions/index.html", data)

def category(request, category):
    data = {
        "category": category,
        "listings": Listing.objects.filter(category=category, isActive=True)
    }
    return render(request, "auctions/index.html", data)

def closed(request):
    data = {
        "listings": Listing.objects.filter(isActive=False)
    }
    return render(request, "auctions/index.html", data)

def watchlist(request):
    listings = Listing.objects.filter(watchlist__user=request.user)
    data = {
        "listings": listings
    }
    return render(request, "auctions/index.html", data)

def categories(request):
    data = {
        "categories": Category.objects.all()
    }
    return render(request, "auctions/categories.html", data)
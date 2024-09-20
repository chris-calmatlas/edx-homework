from django.contrib import admin
from auctions.models import User, Listing, Watchlist, Bid, Comment, Category

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class ListingAdmin(admin.ModelAdmin):
    pass

class WatchlistAdmin(admin.ModelAdmin):
    pass

class BidAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)

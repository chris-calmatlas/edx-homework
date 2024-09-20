from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):  
    title = models.CharField(max_length=64, default="")
    description = models.TextField(max_length=600, default="")
    startingAmount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    imageUrl = models.URLField(blank=True, default="")
    category = models.ForeignKey("Category", blank=True, null=True, on_delete=models.PROTECT)
    user = models.ForeignKey("User", default="", on_delete=models.CASCADE)
    isActive = models.BooleanField(default="True")
    createdOn = models.DateTimeField(auto_now_add=True)
    winningBid = models.ForeignKey("Bid", blank=True, null=True, on_delete=models.DO_NOTHING, related_name="winner")
    
    def __str__(self):
        return f"{self.title}"
    
class Watchlist(models.Model):
    user = models.ForeignKey("User", default="", on_delete=models.CASCADE, unique=True)
    listings = models.ManyToManyField("Listing", blank=True, null=True)

class Bid(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    user = models.ForeignKey("User", default="", on_delete=models.CASCADE)
    listing = models.ForeignKey("Listing", default="", on_delete=models.CASCADE, related_name="bids")
    createdOn = models.DateTimeField(auto_now_add=True)
    isHighest = models.BooleanField(default="True")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['listing'], condition=models.Q(isHighest=True), name="only_one_winning_bid"),
        ]
        ordering = ['-amount']
        
    def __str__(self):
        return f"{self.listing.title} : {self.amount} by {self.user.username}"

class Comment(models.Model):
    user = models.ForeignKey("User", default="", on_delete=models.CASCADE)
    listing = models.ForeignKey("Listing", default="", on_delete=models.CASCADE)
    content = models.TextField(max_length=600, default="")
    createdOn = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    title = models.CharField(max_length=64, default="", primary_key=True)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural = "categories"
    

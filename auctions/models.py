from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Bid(models.Model):
    bid = models.FloatField(default=0)
    userBid = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="uBid")

    def __str__(self):
        return str(self.bid)
    
class Listing(models.Model):
    title = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=300, null=True)
    activeState = models.BooleanField(default=True)
    inicialBid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidValue")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name="categories")
    image = models.CharField(max_length=600, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="userWatchlist")
    def __str__(self):
        return self.title

class Comments(models.Model):
    userComment = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listingComment = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    commentText = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.userComment} commented on {self.listingComment}"
    

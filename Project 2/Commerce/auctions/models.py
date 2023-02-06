from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.category}"


# * Auction listing
class AuctionListings(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    start_bid = models.FloatField()
    bid_raise = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(
        Categories, on_delete=models.PROTECT, related_name="classification")
    image_url = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    watchlist = models.ManyToManyField(
        User, blank=True, related_name="buy_later")
    close = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}(created by {self.seller})"


# * Auction comment
class AuctionComments(models.Model):
    listing = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name="reviewer")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewer")
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} comment {self.comment} at {self.listing}"


# * Auction bid
class AuctionBids(models.Model):
    listing = models.ForeignKey(
        AuctionListings, on_delete=models.CASCADE, related_name="list")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.FloatField()

    def __str__(self):
        return f"{self.user} bid {self.listing} to ${self.bid}"
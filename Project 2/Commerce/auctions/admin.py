from django.contrib import admin
from .models import AuctionListings, User, Categories, AuctionComments, AuctionBids


# ! Class here

class AuctionsListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "title", "category", "created_on", "close")
    filter_horizontal = ("watchlist",)


# ? List Categories
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category")


# ? List Comments
class AuctionCommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "comment", "created_on")


# ? List Bids
class AuctionBidsAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "bid")


# ! Register your models here.

admin.site.register(AuctionListings, AuctionsListingsAdmin)
admin.site.register(User)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(AuctionComments, AuctionCommentsAdmin)
admin.site.register(AuctionBids, AuctionBidsAdmin)

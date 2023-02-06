from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListings, Categories, AuctionComments, AuctionBids


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListings.objects.all(),
        "bids": AuctionBids.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# * Create listing
@login_required
def create_listing(request):
    # User submit form
    if request.method == "POST":
        # Add listing and bid via the submitted form data
        new_listing = AuctionListings(
            seller=User.objects.get(id=request.user.id),
            title=request.POST["title"],
            description=request.POST["description"],
            start_bid=format(float(request.POST["start_bid"]), ".2f"),
            category=Categories.objects.get(id=request.POST["category"]),
            image_url=request.POST["image_url"])
        # Save new list and bid
        new_listing.save()

        # Redirect to index
        return HttpResponseRedirect(reverse("index"))

    # User access page
    else:
        return render(request, "auctions/create_listing.html", {
            "categories": Categories.objects.all()})


# * Listing page
def listing_page(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    comments = AuctionComments.objects.filter(listing=listing)
    bid = AuctionBids.objects.filter(listing=listing)
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comments": comments,
        "largest_bid": bid.order_by('-bid').first(),
        "count_bid": bid.count()
    })


# * Watchlist
@login_required
def watchlist(request):
    # Access current user
    user = User.objects.get(pk=int(request.user.id))

    # User submit "Add to watchlist"
    if request.method == "POST":
        # Get the listing from the form data
        listing = AuctionListings.objects.get(
            pk=int(request.POST["listing_id"]))
        # Add user to listing's watchlist
        listing.watchlist.add(user)

        # Redirect user to listing page
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))

    # User visit watchlist page
    else:
        return render(request, "auctions/watchlist.html", {
            "listings": user.buy_later.all()
        })


# * Remove watchlist
@login_required
def remove(request):
    # Access current user
    user = User.objects.get(pk=int(request.user.id))

    # User submit remove from watchlist
    if request.method == "POST":
        # Get the listing from the form data
        listing = AuctionListings.objects.get(
            pk=int(request.POST["listing_id"]))
        # Remove user to listing's watchlist
        listing.watchlist.remove(user)

        # Redirect user to listing page
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))


# * Show each categories
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all()
    })


# * View listing via category
def category(request, category_id):
    category = Categories.objects.get(id=category_id)
    # category_name = category.category
    return render(request, "auctions/category.html", {
        "listings": AuctionListings.objects.filter(category=category_id),
        "category": category.category
    })


# * Allow users comment below listings
def comments(request):
    # User submit comment
    if request.method == "POST":
        listing = AuctionListings.objects.get(id=request.POST["listing"])
        # Save new comments via the submitted form data
        new_comment = AuctionComments(
            listing=listing,
            user=User.objects.get(id=request.user.id),
            comment=request.POST["comment"]
        )
        new_comment.save()

        # Redirect to listing page
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))


# * Allow users bid listings
def bids(request):
    # User submit bid
    if request.method == "POST":
        listing = AuctionListings.objects.filter(id=request.POST["listing"])
        bid = format(float(request.POST["place_bid"]), ".2f")
        # Save new bid via the submitted form data
        new_bid = AuctionBids(
            listing=listing[0],
            user=User.objects.get(id=request.user.id),
            bid=bid
        )
        new_bid.save()

        # Update listing bid raise
        listing.update(bid_raise=bid)

        # Redirect to listing page
        return HttpResponseRedirect(reverse("listing_page", args=(listing[0].id,)))


def close_auction(request):
    # Seller submit close auction
    if request.method == "POST":
        listing = AuctionListings.objects.filter(id=request.POST["listing"])

        # Update listing has close
        listing.update(close=True)

        # Redirect to listing page
        return HttpResponseRedirect(reverse("listing_page", args=(listing[0].id,)))

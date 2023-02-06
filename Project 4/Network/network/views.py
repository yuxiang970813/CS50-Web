from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse


from .models import User, Posts, UserFollowing


# class IndexListView(ListView):
#     template_name = "network/index.html"
#     paginate_by = 2
#     queryset = Posts.objects.all().order_by("-created_time")


def index(request):
    posts = Posts.objects.all().order_by("-created_time")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        # Add new post
        post = Posts.objects.create(
            user=request.user,
            content=request.POST["content"]
        )
        post.save()
        # Redirect to index
        return HttpResponseRedirect(reverse("index"))


def user_profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)

    # Find follow or not
    try:
        UserFollowing.objects.get(
            follower=request.user,
            target=user_profile
        )
        is_following = True
    except:
        is_following = False

    # Page object
    posts = Posts.objects.filter(user=user_profile).order_by("-created_time")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/user_profile.html", {
        "user_profile": user_profile,
        "page_obj": page_obj,
        "following_count": UserFollowing.objects.filter(follower=user_profile).count(),
        "followers_count": UserFollowing.objects.filter(target=user_profile).count(),
        "is_following": is_following
    })


@login_required
def follow(request):
    # ?User press follow/unfollow button
    if request.method == "POST":

        # ?For later use
        follower = request.user
        status = request.POST["status"]
        target = User.objects.get(pk=request.POST["following"])

        # *Follow
        if status == "Follow":
            follow_status = UserFollowing.objects.create(
                follower=follower, target=target
            )
            follow_status.save()

        # *Unfollow
        elif status == "Unfollow":
            follow_status = UserFollowing.objects.get(
                follower=follower, target=target
            )
            follow_status.delete()

        # *Redirect to target profile
        return HttpResponseRedirect(reverse("user_profile", args=(target.id,)))


@login_required
def following_page(request):
    # ?Page object
    posts = Posts.objects.filter(
        user__being_followed__follower=request.user).order_by("-created_time")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following_page.html", {
        "page_obj": page_obj
    })


@login_required
def like(request, post_id):
    # *Query for requested post
    try:
        post = Posts.objects.get(pk=int(post_id))
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=400)

    # *Update liker
    if request.method == "GET":
        post.liker.add(request.user)
        liker_count = post.liker.count()

        return JsonResponse({
            "message": "Post like successfully.",
            "liker_count": liker_count
        }, status=201)


@login_required
def unlike(request, post_id):
    # *Query for request post
    try:
        post = Posts.objects.get(pk=int(post_id))
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=400)

    # *Remove liker
    if request.method == "GET":
        post.liker.remove(request.user)
        liker_count = post.liker.count()

        return JsonResponse({
            "message": "Post unlike successfully.",
            "liker_count": liker_count
        }, status=201)

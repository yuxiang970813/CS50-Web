from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("user_profile/<int:user_id>", views.user_profile, name="user_profile"),
    path("follow", views.follow, name="follow"),
    path("following_page", views.following_page, name="following_page"),

    # API Routes
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike")
]

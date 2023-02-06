from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="poster")
    content = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    liker = models.ManyToManyField(User, blank=True, related_name="liked_post")

    def __str__(self):
        return f"{self.user} post at {self.created_time}"

    # !Def below are for testcase
    def default_like_is_zero(self):
        return self.likes == 0

    def test_content(self):
        return self.content


class UserFollowing(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="being_followed")

    def __str__(self):
        return f"{self.follower} following {self.target}"

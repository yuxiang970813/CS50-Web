from django.contrib import admin
from .models import User, Posts, UserFollowing

# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(UserFollowing)

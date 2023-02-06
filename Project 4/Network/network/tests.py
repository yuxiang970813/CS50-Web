from django.test import TestCase, Client
from .models import User, Posts


# Create your tests here.

class NewPostTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="test", email="test@test.com", password="test")
        post = Posts.objects.create(user=user, content="Testing123")

    def test_post_valid(self):
        user = User.objects.get(username="test")
        post = Posts.objects.get(user=user)

        self.assertTrue(post.default_like_is_zero())

    def test_content_correct(self):
        user = User.objects.get(username="test")
        post = Posts.objects.get(user=user)
        self.assertEqual(post.test_content(), "Testing123")

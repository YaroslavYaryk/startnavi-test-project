import json
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from blog.models import Post, PostLike


class BaseTests(APITestCase):
    fixtures = ["db_fixtures/blog_post.json", "db_fixtures/users.json", "db_fixtures/blog_like.json"]

    def setUp(self) -> None:
        self.client = APIClient()

        self.credentials = {
            "email": "user1@user.com", "password": "user"
        }

        response = self.client.post(reverse("token_obtain_pair"), data=json.dumps(self.credentials),
                                    content_type="application/json")

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')


class PostTests(BaseTests):

    def setUp(self) -> None:
        super().setUp()
        self.last_post = Post.objects.last()

    def test_posts_list(self):
        response = self.client.get(reverse("get_all_posts"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 9)
        self.assertTrue(response.data["next"])

    def test_create_post(self):
        data = {
            "title": "title 1",
            "body": "body 1",
        }
        response = self.client.post(reverse("create_one_post"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "title 1")
        self.assertEqual(response.data["body"], "body 1")

    def test_change_post(self):
        data = {
            "title": "title 1 changed",
            "body": "body 1 changed",
        }

        response = self.client.patch(reverse("edit_one_post", kwargs={"pk": self.last_post.id}), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "title 1 changed")
        self.assertEqual(response.data["body"], "body 1 changed")

    def test_delete_post(self):
        response = self.client.delete(reverse("delete_one_post", kwargs={"pk": self.last_post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")


class PostLikeTests(BaseTests):

    def setUp(self) -> None:
        super().setUp()
        self.last_post = Post.objects.last()
        self.last_Like = PostLike.objects.last()
        self.user = get_user_model().objects.get(email="user1@user.com")
        self.new_like = PostLike.objects.create(user=self.user, post=self.last_post)

    def test_like_analytics(self):
        url = f"{reverse('get_likes_analytics')}?date_from=2023-03-01&date_to=2023-03-04"

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tuple(response.data["results"][0].keys()), ("date", "likes"))

    def test_like_post(self):
        response = self.client.post(reverse("like_post", kwargs={"post_id": self.last_post.id}), format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["like_id"])

    def test_unlike_post(self):
        response = self.client.post(reverse("unlike_post", kwargs={"post_id": self.last_post.id}), format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "successful")

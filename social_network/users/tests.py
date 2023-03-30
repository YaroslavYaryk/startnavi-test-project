import json
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from blog.tests import BaseTests


class UserTestTests(BaseTests):

    def setUp(self) -> None:
        super().setUp()

    def test_user_info(self):
        response = self.client.get(reverse("get_user_info"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get("id"))
        self.assertTrue(response.data.get("email"))

    def test_change_user_info(self):
        data = {
            "first_name": "Yaryk",
            "last_name": "Dykhanov",
        }

        response = self.client.patch(reverse("change_user_info"), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Yaryk")
        self.assertEqual(response.data["last_name"], "Dykhanov")

    #
    def test_user_activity(self):
        response = self.client.get(reverse("get_user_activity"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get("last_request"))
        self.assertTrue(response.data.get("last_login"))


class AuthTests(APITestCase):
    fixtures = ["db_fixtures/blog_post.json", "db_fixtures/users.json", "db_fixtures/blog_like.json"]

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user(self):
        data = {
            "email": "1@1.com",
            "password": "password",
        }
        response = self.client.post(reverse("create_user"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get("user_id"))
        self.assertEqual(response.data.get("email"), "1@1.com")

    def test_login(self):
        self.credentials = {
            "email": "user1@user.com", "password": "user"
        }

        response = self.client.post(reverse("token_obtain_pair"), data=json.dumps(self.credentials),
                                    content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get("access"))
        self.assertTrue(response.data.get("refresh"))

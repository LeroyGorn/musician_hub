from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import ForumUser
from music.models import ForumCategory, ForumPosted


class TestAPI(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.post = ForumPosted.objects.create(
            title="test", description="TEST", category=ForumCategory.objects.create(name="Test")
        )

    def test_post_list(self):
        user = ForumUser.objects.create(email="admin@admin.com", password="admin")
        print(user)
        self.client.force_authenticate(user=user)

        result = self.client.get(
            reverse(
                "api:post",
                kwargs={
                    "uuid": self.post.uuid,
                },
            )
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, {"id": 1, "title": "test", "description": "TEST", "content": "", "thread": []})

    def test_post_list_wrong_user(self):
        result = self.client.get(
            reverse(
                "api:post",
                kwargs={
                    "uuid": self.post.uuid,
                },
            )
        )
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

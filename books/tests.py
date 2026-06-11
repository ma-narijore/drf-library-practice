from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book


User = get_user_model()


class BookPermissionTests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="T", author="A", cover="HARD", inventory=5, daily_fee="1.50",
        )
        self.list_url = reverse("book-list")
    def test_list_is_public(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    def test_create_forbidden_for_anonymous(self):
        res = self.client.post(self.list_url, {
            "title": "X", "author": "Y", "cover": "SOFT",
            "inventory": 1, "daily_fee": "2.00",
        })
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED,
                                        status.HTTP_403_FORBIDDEN))
    def test_create_allowed_for_admin(self):
        admin = User.objects.create_superuser(email="a@test.com", password="x")
        self.client.force_authenticate(admin)
        res = self.client.post(self.list_url, {
            "title": "X", "author": "Y", "cover": "SOFT",
            "inventory": 1, "daily_fee": "2.00",
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

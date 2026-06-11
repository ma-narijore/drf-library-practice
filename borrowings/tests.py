from datetime import date
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book
from borrowings.models import Borrowing


User = get_user_model()


def make_borrowing(user, book, returned=False):
    # actual_return_date is NOT NULL in the schema, so we must always set it.
    return Borrowing.objects.create(
        borrow_date=date(2026, 1, 1),
        expected_return_date=date(2026, 1, 10),
        actual_return_date=date(2026, 1, 5) if returned else date(2026, 1, 1),
        book=book,
        user=user,
    )
class BorrowingQuerysetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="u@test.com", password="x")
        self.other = User.objects.create_user(email="o@test.com", password="x")
        self.book = Book.objects.create(
            title="T", author="A", cover="HARD", inventory=5, daily_fee="1.5")
        self.url = reverse("borrowing-list")
    def test_user_sees_only_own(self):
        make_borrowing(self.user, self.book)
        make_borrowing(self.other, self.book)
        self.client.force_authenticate(self.user)
        res = self.client.get(self.url)
        self.assertEqual(len(res.data), 1)
    def test_admin_filter_by_user_id(self):
        make_borrowing(self.user, self.book)
        make_borrowing(self.other, self.book)
        admin = User.objects.create_superuser(email="a@test.com", password="x")
        self.client.force_authenticate(admin)
        res = self.client.get(self.url, {"user_id": self.user.id})
        self.assertEqual(len(res.data), 1)

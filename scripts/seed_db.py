from django.contrib.auth import get_user_model
from books.models import Book
from borrowings.models import Borrowing
from datetime import date

User = get_user_model()


def run():

    user = User.objects.create_user(
        email="users1@test.com",
        password="123456",
        first_name="John",
        last_name="Doe"
    )

    admin = User.objects.create_superuser(
        email="admin@test.com",
        password="admin123"
    )

    # books
    book1 = Book.objects.create(
        title="Clean Code",
        author="Robert C. Martin",
        cover="HARD",
        inventory=5,
        daily_fee=1.5
    )

    book2 = Book.objects.create(
        title="Django for APIs",
        author="William S. Vincent",
        cover="SOFT",
        inventory=3,
        daily_fee=2.0
    )

    # borrowing
    Borrowing.objects.create(
        borrow_date=date.today(),
        expected_return_date=date(2026, 6, 10),
        actual_return_date=date(2026, 7, 10),
        book=book1,
        user=user
    )

    print("✅ DB seeded")

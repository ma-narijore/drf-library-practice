from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="u@test.com", password="pass123")
        self.assertEqual(user.email, "u@test.com")
        self.assertTrue(user.check_password("pass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="pass123")
    def test_email_normalized(self):
        user = User.objects.create_user(email="u@TEST.COM", password="x")
        self.assertEqual(user.email, "u@test.com")  # domain lowercased
    def test_create_superuser(self):
        admin = User.objects.create_superuser(email="a@test.com", password="x")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError, PermissionDenied
from accounts.validators import validate_password_strength, validate_mobile_phone, validate_email_format


class AccountsAndSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin", password="admin123", email="admin@ruffyworld.com")
        self.regular_user = User.objects.create_user(username="normaluser", password="UserPass123!@#", email="user@ruffyworld.com")

    def test_password_strength_validation(self):
        # Weak (1 or 2 criteria)
        with self.assertRaises(ValidationError):
            validate_password_strength("weak")
        with self.assertRaises(ValidationError):
            validate_password_strength("weak123")

        # Medium (3 criteria)
        with self.assertRaises(ValidationError):
            validate_password_strength("Medium1")
        with self.assertRaises(ValidationError):
            validate_password_strength("onlylowercase123")

        # Strong (4 criteria)
        try:
            validate_password_strength("StrongPass123")
        except ValidationError:
            self.fail("StrongPass123 should be accepted as Strong!")

        # Very Strong (5 criteria)
        try:
            validate_password_strength("VeryStrongPass123!@#")
        except ValidationError:
            self.fail("VeryStrongPass123!@# should be accepted as Very Strong!")

    def test_phone_validation(self):
        # Valid Bangladeshi numbers
        self.assertEqual(validate_mobile_phone("01712345678"), "01712345678")
        self.assertEqual(validate_mobile_phone("+8801812345678"), "+8801812345678")
        self.assertEqual(validate_mobile_phone("01912-345678"), "01912345678")

        # Invalid numbers
        with self.assertRaises(ValidationError):
            validate_mobile_phone("12345")
        with self.assertRaises(ValidationError):
            validate_mobile_phone("01234567890") # 012 is invalid operator prefix in BD
        with self.assertRaises(ValidationError):
            validate_mobile_phone("invalid_phone")
        with self.assertRaises(ValidationError):
            validate_mobile_phone("0171234567") # only 10 digits

    def test_email_validation(self):
        # Valid email
        self.assertEqual(validate_email_format("test@example.com"), "test@example.com")
        self.assertEqual(validate_email_format("user.name+tag@domain.co.uk"), "user.name+tag@domain.co.uk")

        # Invalid emails
        with self.assertRaises(ValidationError):
            validate_email_format("invalidemail")
        with self.assertRaises(ValidationError):
            validate_email_format("user@")
        with self.assertRaises(ValidationError):
            validate_email_format("@domain.com")
        with self.assertRaises(ValidationError):
            validate_email_format("user@domain") # no valid TLD

    def test_forgot_password_view_accessible(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Forgot Password")

    def test_profile_verification_password_reset_flow(self):
        # 1. Non-existent account
        response = self.client.post(reverse('forgot_password'), {'identity': 'unknown_user_999'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No registered account found")

        # 2. Valid account verification
        response = self.client.post(reverse('forgot_password'), {'identity': 'normaluser'})
        self.assertRedirects(response, reverse('reset_password_direct'))

        # 3. Direct reset password page accessible with active session
        response = self.client.get(reverse('reset_password_direct'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "normaluser")

        # 4. Submit matching strong new password
        reset_response = self.client.post(reverse('reset_password_direct'), {
            'new_password1': 'BrandNewPass123!@#',
            'new_password2': 'BrandNewPass123!@#',
        })
        self.assertRedirects(reset_response, reverse('login'))

        # 5. Verify user can now authenticate with new password
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password('BrandNewPass123!@#'))

    def test_custom_admin_panel_access_and_credentials(self):
        # Unauthenticated user cannot access admin panel dashboard
        response = self.client.get(reverse('custom_admin:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('custom_admin:login'), response.url)

        # Login with admin / admin123
        login_response = self.client.post(reverse('custom_admin:login'), {
            'username': 'admin',
            'password': 'admin123',
        })
        self.assertRedirects(login_response, reverse('custom_admin:dashboard'))

        # Dashboard loads successfully
        dash_response = self.client.get(reverse('custom_admin:dashboard'))
        self.assertEqual(dash_response.status_code, 200)
        self.assertContains(dash_response, "Overview Dashboard")

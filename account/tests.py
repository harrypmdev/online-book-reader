from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm
from .views import login_view


class TestRegisterForm(TestCase):
    """Tests for the account app's RegisterForm."""

    def setUp(self):
        """Set up method for TestRegisterForm."""
        self.register_form = RegisterForm(
            {
                "username": "existingUser",
                "email": "existingEmail@gmail.com",
                "password1": "existingUniquePassword123%",
                "password2": "existingUniquePassword123%",
            }
        )

    def test_form_is_valid(self):
        """Test that register form evaluates valid when given valid data."""
        self.assertTrue(
            self.register_form.is_valid(), msg="Register form is not valid."
        )

    def test_duplicate_email_is_not_valid(self):
        """Test that register form evaluates as not valid when given email
        that is already registered.
        """
        self.register_form.save()
        register_form_to_test = RegisterForm(
            {
                "username": "myuniqueusernamenumbertwo",
                "email": "existingEmail@gmail.com",  # Email is the same
                "password1": "myUniquePassword1234%",
                "password2": "myUniquePassword1234%",
            }
        )
        self.assertTrue(
            not register_form_to_test.is_valid(), msg="Register form is valid."
        )


class TestProfileView(TestCase):
    """Tests for the account app's profile page/view."""

    def setUp(self):
        """Set up method for TestProfileView."""
        self.user = User.objects.create(username="existingUser", email="test@gmail.com")
        self.user.set_password("userPassword123%")
        self.user.save()

    def test_render_valid_profile_page(self):
        """Test that profile page displays user information when
        user is logged in.
        """
        self.client.login(username="existingUser", password="userPassword123%")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200, msg="Profile page not returned.")
        self.assertIn(
            b"existingUser",
            response.content,
            msg="Profile page did not render username.",
        )
        self.assertIn(
            b"test@gmail.com",
            response.content,
            msg="Profile page did not render email.",
        )

    def test_invalid_profile_page(self):
        """Test that profile page redirects to home when user
        is not logged in.
        """
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, "/", msg_prefix="Did not redirect to home.")


class TestLoginView(TestCase):
    """Tests for the account app's login page/view."""

    def setUp(self):
        """Set up method for TestLoginView."""
        self.user = User.objects.create(username="existingUser", email="test@gmail.com")
        self.user.set_password("userPassword123%")
        self.user.save()

    def test_valid_login_page(self):
        """Test that unauthenticated user will receive login
        page when accessing /login/.
        """
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200, msg="Login page not returned.")
        self.assertIn(
            b"Log In", response.content, msg="Login page did not render log in form."
        )
        self.assertIn(
            b"submit", response.content, msg="Login page did not render log in form."
        )

    def test_invalid_login_page(self):
        """Test that authenticated user will receive redirect
        to profile page from login view.
        """
        self.client.login(username="existingUser", password="userPassword123%")
        response = self.client.get(reverse("login"))
        self.assertRedirects(
            response, "/profile/", msg_prefix="Did not redirect to profile."
        )

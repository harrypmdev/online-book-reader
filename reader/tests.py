import json
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.urls import reverse
from books.models import Book, UserBook
from .views import ajax_book_info, ajax_update_progress


class TestReadView(TestCase):
    """Tests for the reader app's read page/view."""

    def setUp(self):
        """Set up method for TestReadView."""
        self.user = User.objects.create(username="existingUser", email="test@gmail.com")
        self.user.set_password("userPassword123%")
        self.user.save()
        url = "https://www.gutenberg.org/cache/epub/74989/pg74989.txt"
        book = Book.objects.create(url=url)
        book.scan()
        book.save()
        self.user_book = UserBook.objects.create(
            book=book, user=self.user, title="Bill Porter", author="Upton Sinclair"
        )
        self.user_book.save()

    def test_render_valid_read_page(self):
        """Test that the read page renders correctly when given
        valid input and the user is authenticated.
        """
        self.client.login(username="existingUser", password="userPassword123%")
        response = self.client.get(reverse("read", args=[self.user_book.id]))
        self.assertEqual(response.status_code, 200, msg="Read page not returned.")
        self.assertIn(
            bytes(self.user_book.title, encoding="utf-8"),
            response.content,
            msg="Read page did not render book.",
        )

    def test_invalid_read_page(self):
        """Test that the read page redirects to the home page
        if user is unauthenticated or UserBook id is invalid.
        """
        response = self.client.get(reverse("read", args=[self.user_book.id]))
        self.assertRedirects(response, "/", msg_prefix="Did not redirect to home page.")
        self.client.login(username="existingUser", password="userPassword123%")
        response = self.client.get(reverse("read", args=[150]))
        self.assertRedirects(response, "/", msg_prefix="Did not redirect to dashboard.")


class TestAjaxBookInfoView(TestCase):
    """Tests for the reader app's ajax_book_info view."""

    def setUp(self):
        """Set up method for TestAjaxBookInfoView."""
        self.user = User.objects.create(username="existingUser", email="test@gmail.com")
        self.user.set_password("userPassword123%")
        self.user.save()
        url = "https://www.gutenberg.org/cache/epub/74989/pg74989.txt"
        book = Book.objects.create(url=url)
        book.scan()
        book.save()
        self.user_book = UserBook.objects.create(
            book=book, user=self.user, title="Bill Porter", author="Upton Sinclair"
        )
        self.user_book.save()

    def test_valid_ajax_book_info_input(self):
        """Test that valid JSON input into the ajax_book_info view
        returns a book split into lines.
        """
        request = HttpRequest()
        request.method = "POST"
        request._body = json.dumps({"book_id": self.user_book.id, "num": 25})
        response = ajax_book_info(request).content
        msg = f"View did not return JSON - returned {response}"
        self.assertTrue(_is_json(response), msg=msg)
        book = json.loads(response)
        self.assertFalse(
            book[0] == "Invalid: valid information was not posted.",
            msg="Valid book was not returned.",
        )
        msg = "Valid book was not returned, insufficient length."
        self.assertTrue(len(book) > 50, msg=msg)

    def test_invalid_ajax_book_info_input(self):
        """Test that invalid JSON input into the ajax_book_info view
        returns a message informing of the invalid input.
        """
        request = HttpRequest()
        request.method = "POST"
        request._body = json.dumps({"book_id": 300, "num": 25})
        response = ajax_book_info(request).content
        book = json.loads(response)
        self.assertTrue(
            book["text_list"] == "Invalid: valid information was not posted.",
            msg="Error message was not returned.",
        )


class TestAjaxUpdateProgressView(TestCase):
    """Tests for the reader app's ajax_update_progress view."""

    def setUp(self):
        """Set up method for TestAjaxUpdateProgressView."""
        self.user = User.objects.create(username="existingUser", email="test@gmail.com")
        self.user.set_password("userPassword123%")
        self.user.save()
        url = "https://www.gutenberg.org/cache/epub/74989/pg74989.txt"
        book = Book.objects.create(url=url)
        book.scan()
        book.save()
        self.user_book = UserBook.objects.create(
            book=book, user=self.user, title="Bill Porter", author="Upton Sinclair"
        )
        self.user_book.save()

    def test_valid_ajax_update_progress_input(self):
        """Test that valid JSON input into the ajax_update_progress view
        returns a book split into lines.
        """
        request = HttpRequest()
        request.method = "POST"
        request._body = json.dumps(
            {"book_id": self.user_book.id, "progress": 10, "length": 100}
        )
        request.user = self.user
        response = ajax_update_progress(request).content
        msg = f"View did not return JSON - returned {response}"
        self.assertTrue(_is_json(response), msg=msg)
        book = json.loads(response)
        self.user_book = UserBook.objects.get(id=self.user_book.id)
        self.assertTrue(
            book["completion"] == "Progress updated.",
            msg="Valid message was not returned.",
        )
        self.assertTrue(
            self.user_book.percent_progress == 10,
            msg="Percent progress not update correctly.",
        )
        msg = "Progress was not updated correctly ."
        self.assertTrue(self.user_book.progress == 10, msg=msg)

    def test_invalid_ajax_update_progress_input(self):
        """Test that invalid JSON input into the ajax_update_progress view
        returns a message informing of the error.
        """
        request = HttpRequest()
        request.method = "POST"
        request._body = json.dumps({"book_id": 300, "progress": 10, "length": 100})
        request.user = self.user
        response = ajax_update_progress(request).content
        msg = f"View did not return JSON - returned {response}"
        self.assertTrue(_is_json(response), msg=msg)
        book = json.loads(response)
        self.user_book = UserBook.objects.get(id=self.user_book.id)
        invalid_msg = "Invalid: valid information was not posted."
        self.assertTrue(
            book["completion"] == invalid_msg, msg="Invalid message was not returned."
        )


def _is_json(possible_json):
    try:
        json.loads(possible_json)
        return True
    except TypeError:
        return False

from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .views import add_book
from .models import Book, UserBook

class TestAddBookView(TestCase):
    """Tests for the 'books' app's add book page/view."""

    def setUp(self):
        """Set up method for TestAddBookView."""
        self.user = User.objects.create(
            username="existingUser",
            email="test@gmail.com" 
        )
        self.user.set_password("userPassword123%")
        self.user.save()
    
    def test_render_valid_add_book_page(self):
        """Test that add book page returns page in which books
        can be added when user is authenticated.
        """
        self.client.login(
            username="existingUser",
            password="userPassword123%"
        )
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200,
                        msg="Add book page not returned.")
        self.assertIn(b"Add a new book", response.content,
                      msg="Add book page did not render heading.")
        self.assertIn(b"input", response.content,
                      msg="Add book page did not render URL form.")

    def test_invalid_add_book_page(self):
        """Test that add book page redirects to login page when user
        is not logged in.
        """
        response = self.client.get(reverse('add_book'))
        self.assertRedirects(response, '/login/', 
                            msg_prefix="Did not redirect to login.")

class TestHomeAndDashboardView(TestCase):
    """Tests for the 'books' app's dashboard page/view."""

    def setUp(self):
        """Set up method for TestDashboardView."""
        self.user = User.objects.create(
            username="existingUser",
            email="test@gmail.com" 
        )
        self.user.set_password("userPassword123%")
        self.user.save()
        url = 'https://www.gutenberg.org/cache/epub/74989/pg74989.txt'
        book = Book.objects.create(url=url)
        book.scan()
        book.save()
        self.user_book = UserBook.objects.create(
            book = book,
            user = self.user,
            title = "Bill Porter",
            author = "Upton Sinclair"
        )
        self.user_book.save()
    
    def test_book_appears_on_dashboard(self):
        """Test that dashboard page presents books associated
        with the current user.
        """
        self.client.login(
            username="existingUser",
            password="userPassword123%"
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200,
                        msg="Dashboard page not returned.")
        self.assertIn(b"Bill Porter", response.content,
                      msg="Dashboard page did not render saved book title.")
        self.assertIn(b"Upton Sinclair", response.content,
                      msg="Dashboard page did not render saved book author.")

    def test_home_page_unauthenticated(self):
        """Test that the index page '/' returns the home page if not logged in,
        rather than the dashboard page.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200,
                        msg="Home page not returned.")
        msg = ("Index page did not return basic home "
                + "page when user not logged in.")
        self.assertIn(b"Read books online", response.content, msg=msg)

class TestManageBookView(TestCase):
    """Tests for the 'books' app's manage book page/view."""

    def setUp(self):
        """Set up method for TestManageBookView."""
        self.user = User.objects.create(
            username="existingUser",
            email="test@gmail.com" 
        )
        self.user.set_password("userPassword123%")
        self.user.save()
        url = 'https://www.gutenberg.org/cache/epub/74989/pg74989.txt'
        book = Book.objects.create(url=url)
        book.scan()
        book.save()
        self.user_book = UserBook.objects.create(
            book = book,
            user = self.user,
            title = "Bill Porter",
            author = "Upton Sinclair"
        )
        self.user_book.save()
    
    def test_render_valid_manage_book_page(self):
        """Test that manage book page returns page in which the
        relevant book can be managed.
        """
        self.client.login(
            username="existingUser",
            password="userPassword123%"
        )
        response = self.client.get(reverse('manage_book',
                                    args=[self.user_book.id]))
        self.assertEqual(response.status_code, 200,
                        msg="Manage book page not returned.")
        self.assertIn(b"Bill Porter", response.content,
                      msg="Manage book page did not render title to edit.")
        self.assertIn(b"Upton Sinclair", response.content,
                      msg="Manage book page did not render author to edit.")

    def test_invalid_manage_book_page(self):
        """Test that manage book page redirects to home/dashboard if
        attempting to manage a book that either does not exist or is not the
        current user's book.
        """
        response = self.client.get(reverse('manage_book',
                                    args=[25]))
        msg = "Did not redirect to home/dashboard page."
        self.assertRedirects(response, '/', 
                            msg_prefix=msg)

class TestDeleteBookView(TestCase):
    """Tests for the 'books' app's delete book view."""

    def setUp(self):
        """Set up method for TestManageBookView."""
        self.user = User.objects.create(
            username="existingUser",
            email="test@gmail.com" 
        )
        self.user.set_password("userPassword123%")
        self.user.save()
        url = 'https://www.gutenberg.org/cache/epub/74989/pg74989.txt'
        book = Book.objects.create(url=url)
        book.scan()
        book.save()
        self.user_book = UserBook.objects.create(
            book = book,
            user = self.user,
            title = "Bill Porter",
            author = "Upton Sinclair"
        )
        self.user_book.save()
    
    def test_valid_delete_book(self):
        """Test that book is deleted when valid information is
        given to delete book view. Both UserBook (user's copy)
        and Book itself should be deleted since Book only has 1 reader
        and so if deleted nobody is reading it.
        """
        self.client.login(
            username="existingUser",
            password="userPassword123%"
        )
        response = self.client.get(reverse('delete_book',
                                    args=[self.user_book.id]))
        msg = "Did not redirect to home/dashboard page."
        self.assertRedirects(response, '/', 
                            msg_prefix=msg)
        filter_user_books = UserBook.objects.filter(id=self.user_book.id)
        user_book_exists = filter_user_books.exists()
        self.assertFalse(user_book_exists, msg="User book still exists.")
        filter_books = Book.objects.filter(id=self.user_book.book.id)
        book_exists = filter_books.exists()
        self.assertFalse(user_book_exists, msg="Book still exists.")

    def test_invalid_delete_book(self):
        """Test that user is simply redirected when invalid attempt to
        delete book is submitted, and book is not deleted.
        """
        response = self.client.get(reverse('delete_book',
                                    args=[self.user_book.id]))
        msg = "Did not redirect to home/dashboard page."
        self.assertRedirects(response, '/', 
                            msg_prefix=msg)
        filter_user_books = UserBook.objects.filter(id=self.user_book.id)
        user_book_exists = filter_user_books.exists()
        self.assertTrue(user_book_exists, msg="User book was deleted.")
        filter_books = Book.objects.filter(id=self.user_book.book.id)
        book_exists = filter_books.exists()
        self.assertTrue(user_book_exists, msg="Book was deleted.")
        
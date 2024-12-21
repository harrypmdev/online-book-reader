import urllib.request
import string
import random
import math
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """Stores a single book with a unique URL. Has a many-to-many relationship
    with User via the UserBook junction table.

    Fields:
    url: models.URLField -- must be unique, the URL which links to the book's
                            text file.
    auto_tile: models.CharField -- the automatically generated title for this
                                   book, set by using the 'scan' method. By
                                   default or if no title can be found, is
                                   set to 'No Title Found'.
    auto_tile: models.CharField -- the automatically generated author for this
                                   book, set by using the 'scan' method. By
                                   default or if no title can be found, is
                                   set to 'No Author Found'.

    Public Methods:
    scan -- scan the book's text for a title and author, and set auto_title and
            auto_author to the values found if applicable.
    total_readers -- return the number of readers who have this book on their
                     dashboard.
    average_rating -- return the average rating for this book rounded to the
                      nearest whole number.
    return_split_text_list -- return the book contents split up into a list of
                              strings, with each string being a line of the
                              book no longer than the character width provided.
    """

    url = models.URLField(unique=True)
    auto_title = models.CharField(max_length=400, default="No Title Found")
    auto_author = models.CharField(max_length=200, default="No Author Found")

    def __str__(self):
        """ __str__ magic method, display auto_title and url. """
        return f"{self.auto_title}: {self.url}"

    def scan(self):
        """Scan the book for an automatic title and author.
        Set the instance's auto_title and auto_author attributes to the scanned
        values if values are found.
        """
        data = self._return_text_list(numbered=False)
        done = [False, False]
        three_lines = ["", "", ""]
        for line_number, line in enumerate(data):
            three_lines[0] = three_lines[1]
            three_lines[1] = three_lines[2]
            three_lines[2] = line
            title_result = Book._scan_for_auto("title:", line)
            author_result = Book._scan_for_auto("author:", line)
            if title_result:
                self.auto_title = title_result
                done[1] = True
            if author_result:
                self.auto_author = author_result
                done[0] = True
            if done[0] and done[1]:
                break

    def total_readers(self):
        """Return the number of readers who have this 
        book on their dashboard.
        """
        return UserBook.objects.filter(book=self).count()

    def average_rating(self):
        """Return the average rating for this book rounded 
        to the nearest whole number.
        """
        ratings = Rating.objects.filter(book=self)
        rating_total = 0
        for rating in ratings:
            rating_total += rating.rating
        return 0 if not ratings.count() else round(rating_total / ratings.count())

    def return_split_text_list(self, width_limit):
        """Return the book contents split up into a list of strings, 
        with each string being a line of the book no longer than the character
        width provided. Where applicable, lines start with a tag denoting
        their line number, with the number at the start of the line separated
        from the line's text content by the rare character 𓀴.

        Arguments:
        width_limit: int -- the maximum amount of characters that should be on
                            any one line of the book.

        Returns an array of strings, the book.
        """
        new_text_list = []
        stripped_text = [line.strip() for line in self._return_text_list()]
        for line in stripped_text:
            new_text_list.extend(self._smart_split(line, width_limit))
        return new_text_list

    def _smart_split(self, line, width_limit):
        # Splits a line into smaller lines if over the width limit.
        # Avoids splitting words where possible.
        if len(line) > width_limit:
            rounded_halfway = self._find_halfway(line)
            return_list = []
            if len(line[:rounded_halfway]) > width_limit:
                return_list.extend(
                    self._smart_split(line[:rounded_halfway], width_limit)
                )
            else:
                return_list.append(line[:rounded_halfway])
            if len(line[rounded_halfway:]) > width_limit:
                return_list.extend(
                    self._smart_split(line[rounded_halfway:], width_limit)
                )
            else:
                return_list.append(line[rounded_halfway:])
            return return_list
        return [line]

    def _find_halfway(self, line):
        # Finds the halfway point of a given line.
        rounded_halfway = math.ceil(len(line) / 2)
        new_halfway = rounded_halfway
        try:
            while line[new_halfway] != " ":
                new_halfway += 1
        except IndexError:
            return rounded_halfway
        return new_halfway

    def _return_text_list(self, numbered=True):
        # Fetches the text list from the URL and splits it into lines,
        # numbered where appropriate.
        data = urllib.request.urlopen(self.url)
        if numbered:
            return [f"{i}𓀴" + line.decode("utf-8") for i, line in enumerate(data)]
        else:
            return [line.decode("utf-8") for i, line in enumerate(data)]

    @staticmethod
    def _scan_for_auto(field, line):
        # Scan a specific line for the given field.
        # Returns None is nothing found.
        if field in line.lower():
            line = line.lower().replace(field, "")
            line = string.capwords(line.strip())
            return line


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    author = models.CharField(max_length=200)
    last_viewed = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    percent_progress = models.IntegerField(default=0)
    color = models.CharField(max_length=20, default="primary")

    def __str__(self):
        return f"{self.user}'s {self.title}"

    def update_percent_progress(self, length):
        self.percent_progress = round((int(self.progress) / int(length) * 100))

    def pick_color(self):
        colors = ("primary", "success", "danger", "info")
        self.color = random.choice(colors)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s rating for {self.book.auto_title}: {str(self.rating)}"

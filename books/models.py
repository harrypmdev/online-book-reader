import urllib.request
import string
import random
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    url = models.URLField()
    auto_title = models.CharField(max_length=400, default="No Title Found")
    auto_author = models.CharField(max_length=200, default="No Author Found")

    def __str__(self):
        return f"{self.auto_title}: {self.url}"

    def return_text_list(self):
        data = urllib.request.urlopen(self.url)
        return [line.decode('utf-8') for line in data]

    def scan(self):
        data = self.return_text_list()
        done = [False, False]
        three_lines = ["", "", ""]
        for line_number, line in enumerate(data):
            three_lines[0] = three_lines[1]
            three_lines[1] = three_lines[2]
            three_lines[2] = line
            title_result = Book.scan_for_auto('title:', line)
            author_result = Book.scan_for_auto('author:', line)
            if title_result:
                self.auto_title = title_result
                done[1] = True
            if author_result:
                self.auto_author = author_result
                done[0] = True
            if done[0] and done[1]:
                break

    @staticmethod
    def scan_for_auto(field, line):
        if field in line.lower():
            line = line.lower().replace(field, '')
            line = string.capwords(line.strip())
            return line

class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    author = models.CharField(max_length=200)
    last_viewed = models.DateField(auto_now=True)
    progress = models.FloatField(default=0)
    color = models.CharField(max_length=20, default="primary")

    def __str__(self):
        return f"{self.user}'s {self.title}"
    
    def pick_color(self):
        colors = ("primary",
            "success",
            "danger",
            "info"
        )
        self.color = random.choice(colors)






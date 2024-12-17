import urllib.request
import string
import random
import math
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    url = models.URLField()
    auto_title = models.CharField(max_length=400, default="No Title Found")
    auto_author = models.CharField(max_length=200, default="No Author Found")

    def __str__(self):
        return f"{self.auto_title}: {self.url}"

    def return_text_list(self, numbered=True):
        data = urllib.request.urlopen(self.url)
        if numbered:
            return [f"{i}𓀴" + line.decode('utf-8') for i, line in enumerate(data)]
        else:
            return [line.decode('utf-8') for i, line in enumerate(data)]

    def scan(self):
        data = self.return_text_list(numbered=False)
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
    
    def total_readers(self):
        return UserBook.objects.filter(book=self).count()
    
    def average_rating(self):
        ratings = Rating.objects.filter(book=self)
        rating_total = 0
        for rating in ratings:
            rating_total += rating.rating
        return 0 if not ratings.count() else round(rating_total / ratings.count())
    
    def find_halfway(self, line):
        rounded_halfway = math.ceil(len(line)/2)
        new_halfway = rounded_halfway
        try:
            while line[new_halfway] != " ":
                new_halfway += 1
        except IndexError:
            return rounded_halfway
        return new_halfway

    def smart_split(self, line, width_limit):
        # Returns a list of lines from a single line
        #print(f"{str(len(line))} > {width_limit}: {len(line) > width_limit}")
        if len(line) > width_limit:
            rounded_halfway = self.find_halfway(line)
            return_list = []
            if len(line[:rounded_halfway]) > width_limit:
                return_list.extend(self.smart_split(line[:rounded_halfway], width_limit))  
            else:
                return_list.append(line[:rounded_halfway])     
            if len(line[rounded_halfway:]) > width_limit:
                return_list.extend(self.smart_split(line[rounded_halfway:], width_limit))
            else:
                return_list.append(line[rounded_halfway:])  
            return return_list
        return [line]

    def return_split_text_list(self, width_limit):
        new_text_list = []
        stripped_text = [line.strip() for line in self.return_text_list()]
        for line in stripped_text:
            new_text_list.extend(self.smart_split(line, width_limit))
        with open('local.txt', 'w') as f:
            for line in new_text_list:
                f.write(f"{line}\n")
        return new_text_list
    
    def return_whole_text(self):
        string_data = ""
        for line in return_text_list():
            line.replace("\n", " ")
            string_data.append(line)
        return string_data

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
    last_viewed = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    percent_progress = models.IntegerField(default=0)
    color = models.CharField(max_length=20, default="primary")

    def __str__(self):
        return f"{self.user}'s {self.title}"
    
    def update_percent_progress(self, length):
        self.percent_progress = round((int(self.progress) / int(length)*100))
    
    def pick_color(self):
        colors = ("primary",
            "success",
            "danger",
            "info"
        )
        self.color = random.choice(colors)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s rating for {self.book.auto_title}: {str(self.rating)}"





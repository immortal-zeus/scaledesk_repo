from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime,date, timedelta
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    Student = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','username']


    def __str__(self):
        return f"{self.first_name}"


class Categories(models.Model):
    Category = models.CharField(max_length = 20, blank=True , null=True)

    def __str__(self):
        return f"{self.Category} -{ self.pk}"

class BookModel(models.Model):
    Book_categories= models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, related_name="Genre")
    book_name = models.CharField(max_length = 100, blank=True)
    author = models.CharField(max_length = 30, blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    base_fee = models.PositiveIntegerField(blank=True, null=True)
    current_count = models.PositiveIntegerField(blank=True, null=True)
    no_of_issued = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.book_name, self.Book_categories, self.author, self.current_count, self.no_of_issued}"

class BookInventry(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='Book_detail')
    book_uniqueid = models.CharField(max_length=7, unique=True)
    issued = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.book_uniqueid}"


class BookLogs(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True , related_name='issuer')
    book_inventry = models.ForeignKey(BookInventry, on_delete = models.CASCADE, related_name='id_book')
    issue_day = models.DateField(auto_now_add=True)
    checkback = models.DateField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    Transaction = models.CharField(max_length=10, unique=True)

    def cal(self):
        temp = date.today() - self.due_date
        c = temp.days
        if c >0:
            return self.book_inventry.book.base_fee +(c * self.book_inventry.book.base_fee)
        else:
            return self.book_inventry.book.base_fee

    def __str__(self):
        return f"{self.checkback} , {self.due_date} ,{self.user_id} , {self.pk}"


# trans id --- book return api
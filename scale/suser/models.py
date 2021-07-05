from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Desgniation(models.Model):
    d_name = models.CharField(max_length=10 , unique=True )


    def __str__(self):
        return f"{self.d_name}"

class User(AbstractUser):
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    desgination = models.ForeignKey(Desgniation ,null=True,on_delete=models.CASCADE, related_name="Desgination")
    reports_to = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE, related_name="HigherPosition")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self):
        return f"{self.first_name} - {self.desgination}"


class BookType(models.Model):
    book_type = models.CharField(max_length = 20, blank=True , null=True)

    def __str__(self):
        return f"{self.book_type}"

class BookModel(models.Model):
    book_type_id = models.ForeignKey(BookType, on_delete=models.CASCADE, null=True)
    book_name = models.CharField(max_length = 100, blank=True)
    author = models.CharField(max_length = 50, blank=True, null=True)
    base_fee = models.PositiveIntegerField(blank=True, null=True)
    current_count = models.PositiveIntegerField(blank=True, null=True)
    no_of_issued = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.book_name, self.book_type, self.author, self.current_count, self.no_of_issued}"

class BookInventry(models.Model):
    book = models.CharField(max_length = 50, blank=True, null=True)
    book_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.book, self.book_id}"

class BookLogs(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    book_inventry = models.ForeignKey(BookInventry, on_delete = models.CASCADE)
    issue_day = models.DateTimeField(blank=True, null=True)
    checkback = models.CharField(max_length = 50, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    # fees_to_be_added = models.DateTimeField(blank=True, null=True)
    fine_fee = models.IntegerField(blank=True, null=True)


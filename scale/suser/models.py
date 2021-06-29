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
    getting_report = models.ForeignKey('self',blank=True,null=True, on_delete= models.CASCADE, related_name="LowerPosition")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name' , 'username','number']


    def __str__(self):
        return f"{self.first_name} {self.desgination}"

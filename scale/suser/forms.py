from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *

class Usercus(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'desgination' , 'reports_to','getting_report',)


class Userchan(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'desgination', 'reports_to', 'getting_report',)
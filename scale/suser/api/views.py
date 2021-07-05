from rest_framework import generics

from suser.models import *
from .serializers import UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Userupdate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Userreti(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer





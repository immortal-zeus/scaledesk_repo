from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
   path('',views.UserListView.as_view()),
   path('create',views.Userupdate.as_view()),
   path('<int:pk>',views.Userreti.as_view()),
   path ('Category/',views.Cat),
   path('Book/',views.Bookapi),
   path('checkout/',views.checkout)
]
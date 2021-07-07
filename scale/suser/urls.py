from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('' , views.dashboard,name="dashboard"),
    path('login',views.loginuser, name="login"),
    path('register',views.register,name="register"),
    path('logout', views.loginuser,name="logout"),
    path('booklist',views.booklist,name="booklist"),
    path('bookdetail',views.bookdetail,name="bookdetail"),
    path('api/',include('suser.api.urls')),

]
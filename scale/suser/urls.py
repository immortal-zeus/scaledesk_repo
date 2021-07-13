from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('' , views.index,name="index"),
    path('login',views.loginuser, name="login"),
    path('register',views.register,name="register"),
    path('logout', views.logoutuser,name="logout"),
    path('booklist',views.booklist,name="booklist"),
    path('bookcreate',views.bookcreate,name='create'),
    path('bookcategory',views.bookcategory,name='category'),
    path('bookdetail', views.bookdetail, name = 'bookdetail'),
    path('checkout', views.Checkout, name='checkout'),
    path('bookcheckout', views.BookCheckout, name='Bookcheckout'),
    path('checkoutdone', views.Checkoutdone, name='checkoutdone'),
    path('userlist',views.userlist,name='userlist'),
    path('daywise',views.day_wise, name='day'),
    path('return',views.returnbook,name='returnB'),
    path('rhere',views.rhere, name='rhere'),
    path('userdetail',views.userdetail , name = 'userdetail'),
    path('api/',include('suser.api.urls')),


]
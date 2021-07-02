from django.conf.urls import url
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
   path('',views.UserListView.as_view()),
   path('create',views.Userupdate.as_view()),
   path('<int:pk>',views.Userreti.as_view()),
   path('Desgniation',views.DesListView.as_view()),
   path('Desgniation/create',views.Desupdate.as_view()),
   path('Desgniation/<int:pk>',views.Desreti.as_view())
]
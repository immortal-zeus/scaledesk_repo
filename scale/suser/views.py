from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout , decorators
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db import IntegrityError
# Create your views here.

def index(request):
    return render(request,"suser/index.html")

def loginuser(request):
    if request.method == "POST":
        email_p = request.POST['email']
        password_p = request.POST['password']
        user = authenticate(request, username=email_p, password=password_p)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"suser/login.html",{
                "email": email_p,
                "flag" : True
            })
    return render(request,"suser/login.html")

def register(request):
    if request.method == "POST":
        first_r = request.POST['first_name']
        last_r = request.POST['last_name']
        email_r = request.POST['email']
        password_r = request.POST['password']
        password2_r = request.POST['confirm_password']
        username_r = email_r.split('@')[0]
        if password_r != password2_r:
            return render(request, "suser/register.html",{
                "message": "Passwords must match.",
            })

        try:
            user = User.objects.create_user(first_name = first_r , last_name = last_r, username = username_r ,email = email_r, password = password_r)
            user.save()
        except IntegrityError:
            return render(request, "suser/register.html",{
                "message" : "Email already exist.",
                "first_r": first_r,
                "last_r": last_r,
                "email_r":email_r,
                
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"suser/register.html")




from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout , decorators
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db import IntegrityError
# Create your views here.

@decorators.login_required(login_url='/login')
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
        is_what = request.POST['role']
        username_r = email_r.split('@')[0]
        if password_r != password2_r:
            return render(request, "suser/register.html",{
                "message": "Passwords must match.",
            })

        try:
            if is_what == 'student':
                user = User.objects.create_user(first_name = first_r , last_name = last_r, username = username_r ,email = email_r, password = password_r, Student = True)
            elif is_what == 'admin ':
                user = User.objects.create_user(first_name = first_r , last_name = last_r, username = username_r ,email = email_r, password = password_r, is_superuser = True)
            else:
                user = User.objects.create_user(first_name = first_r , last_name = last_r, username = username_r ,email = email_r, password = password_r, is_staff = True)

            user.save()
        except IntegrityError:
            return render(request, "suser/register.html",{
                "message" : "Email already exist."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"suser/register.html")


def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def booklist(request):
    return render(request,"suser/booklist.html",{
        # "books": BookModel.objects.all(),
        "books" : [1,2,3,4,5],
    })


def bookdetail(request):
    #suraj : wrtie code here
    pass
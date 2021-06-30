from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"suser/index.html")

def login(request):
    return render(request,"suser/login.html")

def register(request):
    return render(request,"suser/register.html")
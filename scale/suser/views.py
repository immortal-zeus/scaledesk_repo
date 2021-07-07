from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout , decorators
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db import IntegrityError
import uuid
# Create your views here.

def random_string(string_length=7):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-","")
    return random[0:string_length]

@decorators.login_required(login_url='/login')
def index(request):
    return render(request,"suser/dashboard.html")

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
            elif is_what == 'admin':
                user = User.objects.create_user(first_name = first_r , last_name = last_r, username = username_r ,email = email_r, password = password_r, is_staff = True, is_superuser = True)
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

def bookcategory(request):
    if request.method == 'POST':
        cat = request.POST['category']
        cate = Categories(Category = cat)
        cate.save()
        return HttpResponseRedirect(reverse('create'))
    return render(request,"suser/bookCategory.html")

def bookcreate(request):
    if request.method == "POST":
        Book_categories = request.POST["categories"]
        book_name = request.POST["book_name"]
        author = request.POST["author"]
        publish_date = request.POST["publish_date"]
        base_fee = request.POST["base_fee"]
        current_count = request.POST["current_count"]
        cat = Categories.objects.get(Category=Book_categories)
        try :
            book = BookModel(Book_categories = cat,book_name=book_name, author =author,publish_date=publish_date,base_fee=base_fee,current_count=current_count, no_of_issued=0)
        except IntegrityError:
            return render(request,"HackerMan")
        book.save()
        create_inven(book_name,author)
        return HttpResponseRedirect(reverse('booklist'))
    return render(request,"suser/bookcreate.html",{
        "categories" : Categories.objects.all(),
    })


def create_inven(bookname, author):
    book = BookModel.objects.get(book_name = bookname, author = author)
    i = 0
    while(True):
        if i== book.current_count:
            break
        temp = random_string()
        a = BookInventry.objects.all().filter(book_uniqueid=temp)
        if a.count() ==0:
            inven = BookInventry(book= book ,book_uniqueid = temp)
            inven.save()
            i +=1
            continue
        else:
            continue


def booklist(request):
    return render(request,"suser/booklist.html",{
        "books": BookModel.objects.all(),
    })


def bookdetail(request):
    #suraj : wrtie code here
    book_id = request.GET.get('bookid', None)
    book = BookModel.objects.get(pk = book_id)
    book_inven = BookInventry.objects.all().filter(book = book)
    log = []
    for b in book_inven:
        temp = BookLogs.objects.all().filter(book_inventry = b)
        if temp.count() ==0:
            continue
        else:
            log.append(temp)

    return render(request,"suser/bookdetail.html",{
        "book": book,
        "Logs": log,

    })



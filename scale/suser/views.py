from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout , decorators
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db import IntegrityError
from .helper import *
from datetime import datetime,date, timedelta
from django.contrib import messages

# Create your views here.

# data table aman

@decorators.login_required(login_url='/login')
def index(request):

    books = BookLogs.objects.all()
    cnt = books.count()

    book_code = []
    i = 0
    while i < cnt:
        b = books[i]
        name = b.book_inventry
        book_code.append(name)
        i = i + 1
    book_code = list(set(book_code))
    # print(book_code)

    dict = {}
    ne_books = []
    for bb in book_code:
        code = BookInventry.objects.all().filter(book_uniqueid = bb)
        one = code[0]
        book_book = one.book
        book_nme = book_book.book_name
        ne_books.append(book_nme)

    dict = {item:ne_books.count(item) for item in ne_books}
    # print(dict)
    topy = list(dict.values())
    topx = list(dict.keys())
    # print(topx,topy)


    checkin = books.filter(checkback__isnull=True)
    issued = checkin.count()

    checkout = books.filter(checkback__isnull=False)
    returned = checkout.count()

    # Past 7 days checkin and checkout
    aa = []   #date
    data1 = []   #issued
    data2 = []   #returnd
    now = datetime.now()
    for x in range(7):
        d = now - timedelta(days=x)
        aa.append(d.date())

    for day in aa:
        try:
            x = BookLogs.objects.all().filter(checkback__isnull=True, due_date=day) #non-returned
            data1.append(x.count())
            y = BookLogs.objects.all().filter(checkback__isnull=False, due_date=day) #returned
            data2.append(y.count())
        except:
            pass
    lable = [l.strftime('%Y-%m-%d') for l in aa]
    # print(lable,data1,data2)


    #Past 5 Non-Returned books
    log = BookLogs.objects.all().filter(checkback__isnull=True).order_by('-due_date')
    aaa = []  # due date book return past
    freq = []  # total book remaing
    for x in range(5):
        try:
            logg = log[x].due_date
            aaa.append(logg)
            c = log.filter(due_date = logg).count()
            freq.append(c)
        except:
            pass
    date = [l.strftime('%Y-%m-%d') for l in aaa]
    print(date,freq)

    return render(request,"suser/dashboard.html",{
        'issued': issued,
        'returned': returned,
    #top 5 books purchase 
        'topx':topx,
        'topy': topy,
    # Past 7 days checkin and checkout
        'lable': lable,
        'data1': data1,
        'data2': data2,
    # Past Non-Returned books
        'date': date,
        'freq': freq,
    })


def loginuser(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            email_p = request.POST['email']
            password_p = request.POST['password']
            user = authenticate(request, username=email_p, password=password_p)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "suser/login.html", {
                    "email": email_p,
                    "flag": True
                })
        return render(request, "suser/login.html")
    else:
        return HttpResponseRedirect(reverse("index"))

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

@decorators.login_required(login_url='/login')
def bookcategory(request):
    if request.method == 'POST':
        cat = request.POST['category']
        cate = Categories(Category = cat)
        cate.save()
        return HttpResponseRedirect(reverse('create'))
    else:
        return HttpResponseRedirect(reverse('index'))

@decorators.login_required(login_url='/login')
def bookcreate(request):
    if request.method == "POST":
        Book_categories = request.POST["categories"]
        book_name = request.POST["book_name"]
        author = request.POST["author"]
        publish_date = request.POST["publish_date"]
        check = publish_date.split('-')
        if date(int(check[0]), int(check[1]) , int(check[2])) > date.today():
            return render(request,"suser/bookcreate.html",{
                "message": "Publish date can not be in the future. "
            })
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



@decorators.login_required(login_url='/login')
def booklist(request):
    return render(request,"suser/booklist.html",{
        "books": BookModel.objects.all(),
    })

@decorators.login_required(login_url='/login')
def bookdetail(request):
    #suraj : wrtie code here
    book_id = request.GET.get('bookid', None)
    book = BookModel.objects.get(pk = book_id)
    book_inven = BookInventry.objects.all().filter(book = book, issued = True )
    log_true = []
    for b in book_inven:
        temp = BookLogs.objects.all().filter(book_inventry = b)
        if temp.count() ==0:
            continue
        else:
            # log_true.append(temp)
            for i in temp:
                log_true.append(i)


    book_inven_false = BookInventry.objects.all().filter(book=book, issued=False)
    log_false = []
    for b in book_inven_false:
        temp = BookLogs.objects.all().filter(book_inventry = b)
        if temp.count() ==0:
            continue
        else:
            # log_true.append(temp)
            for i in temp:
                log_false.append(i)

    return render(request,"suser/bookdetail.html",{
        "book": book,
        "Logs": sort_this(log_true) + sort_this(log_false),
        "count": len(log_true) + len(log_false)

    })

@decorators.login_required(login_url='/login')
def day_wise(request):
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    start = date.today() + timedelta(days=-30)  # future change
    day = BookLogs.objects.all().filter(due_date=today)
    afterdate = BookLogs.objects.all().filter(checkback__isnull=True, due_date__range=[start, yesterday])
    return render(request, "suser/day.html", {
        "day": day,
        "afterdate": afterdate
    })

@decorators.login_required(login_url='/login')
def returnbook(request):
    id = request.GET.get('id', None)
    inven = BookLogs.objects.get(pk = id)
    return render(request,"suser/returnbook.html",{
        "book":inven,
    })

@decorators.login_required(login_url='/login')
def Checkout(request):
    return render(request, 'suser/checkout.html',{
    "books": Categories.objects.all(),
    "user_name" : User.objects.all(),
    })

@decorators.login_required(login_url='/login')
def BookCheckout(request):
    if request.method == 'POST':
        n_ame = request.POST['user_name']
        name = User.objects.get(pk=n_ame)
        bookname = request.POST['book_name']
        bookdata = BookModel.objects.get(book_name=bookname)
        code = BookInventry.objects.all().filter(book=bookdata,issued = False)
        if code.count() == 0:
            messages.success(request, 'No book available at the moment !!!')
            return HttpResponseRedirect('/checkout')
        coded = code[0]
        new = BookInventry.objects.get(book_uniqueid=coded)
        bkdata = bookdata.current_count  #for Total Book Available
        current_time = date.today()
        due_Date = date.today() + timedelta(days=7)
        if bookdata.current_count !=0:
            data = BookLogs(user_id = name, book_inventry=coded, issue_day=current_time, due_date=due_Date , Transaction = str(date.today())[-1]+random_string(8)+str(date.today())[-2])
            data.save()
            new.issued = True
            new.save()
            bookdata.no_of_issued += 1
            bookdata.current_count -= 1
            bookdata.save()
            messages.success(request, 'Successfully book checkout !!!')
            return HttpResponseRedirect('/checkout')
        else:
            messages.success(request, 'No book available at the moment !!!')
            return HttpResponseRedirect('/checkout')


@decorators.login_required(login_url='/login')
def Checkoutdone(request):

    return render(request, 'suser/checkoutdone.html')


@decorators.login_required(login_url='/login')
def rhere(request):
    id = request.GET.get('id', None)
    if id is not None:
        log = BookLogs.objects.get(pk = id)
        log.checkback = date.today()
        total_fine = log.cal()
        log.book_inventry.issued = False
        log.book_inventry.book.current_count +=1
        log.book_inventry.book.no_of_issued -= 1
        log.book_inventry.book.save()
        log.book_inventry.save()

        log.save()
        return render(request,"suser/day.html",{
            "book":log,
            "fee":total_fine,
            "flag":True,

    })

@decorators.login_required(login_url='/login')
def userlist(request):
    return render(request, "suser/userlist.html",{
        'all_users': User.objects.all(),
    })

@decorators.login_required(login_url='/login')
def userdetail(request):
    id = request.GET.get('id', None)
    if id is not None:
        usr = User.objects.get(pk = id)
        all_books = BookLogs.objects.all().filter(user_id = usr)

        return render(request,"suser/userdetail.html",{
            "userq": usr,
            "booksu":all_books,
        })




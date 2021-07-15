from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from suser.models import *
from suser.helper import *
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,date, timedelta

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Userupdate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Userreti(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class Cat(APIView):
    def get(self,request):
        response = {}
        response['status'] = 200
        response['message'] = "Something is wrong."

        try:
            Bookcat = Categories.objects.all()
            payload= []
            for cats in Bookcat:
                payload.append({
                    "Category" : cats.Category,
                })
            response['status'] = 100
            response['message'] = "All Category ."
            response['data'] = payload
        except Exception as e:
            print(e)

        return Response(response)


    @csrf_exempt
    def post(self, request):
        response = {}
        response['status'] = 200
        response['message'] = "Something is wrong."

        try:
            all_data = request.data

            Category = all_data.get('Category')

            if Category is None:
                response['status'] = 404
                response['message'] = "Category is required ."
                raise Exception('Need a Category!')


            Cate_obj = Categories.objects.create(Category = Category)

            payload = {'pk' : Cate_obj.pk,
                       'Category': Cate_obj.Category}
            response['status'] = 100
            response['message'] = "Category is Saved.."
            response['payload'] = payload
        except Exception as e:
            print(e)

        return Response(response)

    # def put(self, request):
    #     response = {}
    #     response['status'] = 200
    #     response['message'] = "Something is wrong."




Cat = Cat.as_view()

class Bookapi(APIView):

    def get(self, request):
        response = {}
        response['status'] = 200
        response['message'] = "Something is wrong."

        try :
            Books = BookModel.objects.all()
            payload = []
            for book in Books:
                payload.append({
                    "Book_categories" : book.Book_categories.Category,
                    "book_name": book.book_name,
                    "author": book.author,
                    "publish_date": book.publish_date,
                    "base_fee":book.base_fee,
                    "checkedin":book.current_count,
                    "checkedout":book.no_of_issued,
                })

            response['status'] = 100
            response['message'] = "All Books ."
            response['data'] = payload
        except Exception as e:
            print(e)

        return Response(response)

    # def post(self, request):
    #     response = {}
    #     response['status'] = 200
    #     response['message'] = "Something is wrong."
    #
    #
    #     try:
    #         all_data = request.data
    #
    #         Category = all_data.get('Category')
    #
    #         if Category is None:
    #             response['status'] = 404
    #             response['message'] = "Category is required ."
    #             raise Exception('Need a Category!')
    #
    #
    #         Cate_obj = Categories.objects.create(Category = Category)
    #
    #         payload = {'pk' : Cate_obj.pk,
    #                    'Category': Cate_obj.Category}
    #         response['status'] = 100
    #         response['message'] = "Category is Saved.."
    #         response['payload'] = payload
    #     except Exception as e:
    #         print(e)
    #
    #     return Response(response)


Bookapi = Bookapi.as_view()
class checkout(APIView):

    @csrf_exempt
    def post(self, request):
        response = {}
        response['status'] = 200
        response['message'] = "Something is wrong."

        try :
            all_data = request.data
            username = all_data.get('user_name')
            user_n = User.objects.get(pk = username)
            book_pk = all_data.get('book_name')
            bookdata = BookModel.objects.get(pk=book_pk)
            code = BookInventry.objects.all().filter(book=bookdata, issued=False)
            if code.count() == 0:
                response['status'] = 205
                response['message'] = "Book out of Stock."
                return Response(response)
            else:
                coded = code[0]
                new = BookInventry.objects.get(book_uniqueid=coded)
                bkdata = bookdata.current_count  # for Total Book Available
                current_time = date.today()
                due_Date = date.today() + timedelta(days=7)
                if bookdata.current_count != 0:
                    data = BookLogs(user_id=user_n, book_inventry=coded, issue_day=current_time, due_date=due_Date ,Transaction= str(date.today())[-1]+random_string(8)+str(date.today())[-2])
                    data.save()
                    new.issued = True
                    new.save()
                    bookdata.no_of_issued += 1
                    bookdata.current_count -= 1
                    bookdata.save()
                    response['status'] = 100
                    response['message'] = "Saved Successfully ."
                    return Response(response)
                else:
                    response['status'] = 205
                    response['message'] = "Book out of Stock."
                    return Response(response)

        except Exception as e:
            print(e)

        return Response(response)



checkout = checkout.as_view()

class getbook(APIView):

    @csrf_exempt
    def post(self,request):
        response = {}
        response['status'] = 200
        response['message'] = "Something is wrong."

        try:
            all_data = request.data
            Category = all_data.get('Category')
            print(Category)
            if Category is None:
                response['status'] = 404
                response['message'] = "Category is required ."
                raise Exception('Need a Category!')

            cat = Categories.objects.get(pk = Category)
            book = BookModel.objects.all().filter(Book_categories = cat)

            # payload = { "book" : book}
            if book.count() == 0:
                response['status'] = 403
                response['message'] = "No Books in this category."
                return Response(response)

            payload =[]
            for b in book :
                payload.append({
                    "pk": b.pk,
                    "book_name" : b.book_name,
                    "author" : b.author,
                    "publish_date": b.publish_date,
                    "base_fee" : b.base_fee,
                    "current_count" :b.current_count,
                    "no_of_issued" :b.no_of_issued,
                })

            response['status'] = 100
            response['message'] = "Book return."
            response['payload'] = payload
            return Response(response)



        except Exception as e:
            print(e)
            return Response(response)



getbook = getbook.as_view()

class returnbook(APIView):

    @csrf_exempt
    def post(self,request):
        response = {}
        response['status'] = 200
        response['message'] = "Something is wrong."

        try:
            all_data = request.data
            pk = all_data.get('pk')
            if pk is not None:
                log = BookLogs.objects.get(pk=pk)
                log.checkback = date.today()
                log.book_inventry.issued = False
                log.book_inventry.book.current_count += 1
                log.book_inventry.book.no_of_issued -= 1
                log.book_inventry.book.save()
                log.book_inventry.save()
                log.save()
                response['status'] = 100
                response['message'] = "Return Successful."
                response['checkback'] = log.checkback
                return Response(response)

            else:
                response['status'] = 404
                response['message'] = "No id given."



        except Exception as e:
            print(e)


        return Response(response)


returnbook = returnbook.as_view()

class trans(APIView):

    @csrf_exempt
    def post(self, request):
        response = {}
        response['status'] = 200
        response['message'] = "Something is wrong."

        try:
            all_data = request.data
            Transaction = all_data.get('trans')
            if Transaction is not None:
                bookt =BookLogs.objects.get(Transaction = Transaction)
                payload = {
                    "user_id" : bookt.user_id.pk,
                    "username" : bookt.user_id.first_name + bookt.user_id.last_name,
                    "book_id" : bookt.book_inventry.book.pk,
                    "bookname" : bookt.book_inventry.book.book_name,
                    "category" : bookt.book_inventry.book.Book_categories.Category,
                    "issue_day" : bookt.issue_day,
                    "checkback" : bookt.checkback,
                    "due_date" : bookt.due_date,
                    "Transaction" : bookt.Transaction
                }

                response['status'] = 100
                response['message'] = "Found."
                response['payload']= payload

                return Response(response)

            else:
                response['status'] = 404
                response['message'] = "Not Found."

                return Response(response)


        except Exception as e:
            print(e)

            return Response(response)

trans = trans.as_view()


class DashChart(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        # print('here')
        books = BookLogs.objects.all()

        book_code = []
        for i in range(len(books)):
            b = books[i]
            name = b.book_inventry
            book_code.append(name)
        book_code = list(set(book_code))
        # print(book_code)

        ne_books = []
        for bb in book_code:
            code = BookInventry.objects.all().filter(book_uniqueid = bb)
            book_book = code[0].book.book_name
            ne_books.append(book_book)

        dict = {item:ne_books.count(item) for item in ne_books}
        # print(dict)
        topy = list(dict.values()) 
        topy = topy[:5]
        topx = list(dict.keys())
        topx = topx[:5]
        # print(topx,topy)  ########################


        # Total issued & returned
        checkin = books.filter(checkback__isnull=True)
        issued = checkin.count()

        checkout = books.filter(checkback__isnull=False)
        returned = checkout.count()
        # print(issued,returned)  ######################

        # Past 7 days checkin and checkout
        aa = []   #date
        data1 = []   #issued
        data2 = []   #returnd
        now = datetime.now()
        for x in range(7):
            d = now - timedelta(days=x)
            aa.append(d.date())
        # print(aa)
        for day in aa:
            # try:
            x = books.filter(issue_day=day) #issued
            data1.append(x.count())
            y = books.filter(checkback=day) #returned
            data2.append(y.count())
            # except:
            #     pass
        lable = [l.strftime('%Y-%m-%d') for l in aa] 
        # print(lable,data1,data2)     ######################


        #Past 5 Non-Returned books
        log = BookLogs.objects.all().filter(checkback__isnull=True).order_by('-due_date')
        aaa = []  # due date book return past
        freq = []  # total book remaing

        for x in range(len(log)):
            logg = log[x].due_date
            aaa.append(logg)

        aaa = list(set(aaa))
        aaa = sorted(aaa)
        aa = []
        for i in range(len(aaa)):
            logg = aaa[i]
            aa.append(aaa[i])
            c = log.filter(due_date = logg).count()
            freq.append(c)

        date = [l.strftime('%Y-%m-%d') for l in aa]
        date = date[:7]
        freq = freq[:7]
        # print(date,freq) ############################


        #converting json data format

        Books_info = [{'issued': issued,'returned':returned}]

        Top_books = []
        for i in range(len(topx)):
            Top_books.append({'topx': topx[i],'topy':topy[i]})
        # print(Top_books)

        Past_seven_days = []
        for i in range(len(lable)):
            Past_seven_days.append({'lable': lable[i],'data1':data1[i],'data2':data2[i]})
        # print(Past_seven_days)

        Past_Non_Returned = []
        for i in range(len(date)):
            Past_Non_Returned.append({'date': date[i],'freq':freq[i]})
        # print(Past_Non_Returned)

        context = {
            'Past_Non_Returned': Past_Non_Returned,
            'Books_info': Books_info,
            'Top_books' : Top_books,
            'Past_seven_days' : Past_seven_days
        }


        return Response(context) 
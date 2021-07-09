from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from suser.models import *
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
            book = all_data.get('book_name')
            bookdata = BookModel.objects.get(book_name=book)
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
                    data = BookLogs(user_id=user_n, book_inventry=coded, issue_day=current_time, due_date=due_Date)
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
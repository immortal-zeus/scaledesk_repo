from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from suser.models import *
from .serializers import UserSerializer

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
import uuid
from .models import *

def random_string(string_length=7):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-","")
    return random[0:string_length]

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


def sort_this(log):
    temp = sorted(log , key= lambda x : x.due_date )
    return temp




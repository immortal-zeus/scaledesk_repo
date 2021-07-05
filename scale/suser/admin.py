from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import Usercus , Userchan
User = get_user_model()
from .models import BookLogs, BookInventry, BookModel, BookType
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = Usercus
    form = Userchan
    model = User
    list_display = ('email', 'first_name', 'desgination','reports_to',)
    list_filter = ('email','first_name', 'desgination','reports_to',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Position_Status', {'fields':('desgination','reports_to',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
        ),
    )
    search_fields = ('email','desgination','reports_to',)
    ordering = ('email',)


admin.site.register(User,CustomUserAdmin)

admin.site.register(Desgniation)


@admin.register(BookType)
class BookTypeModel(admin.ModelAdmin):
    list_display = ['id', 'book_type']

@admin.register(BookInventry)
class BookInventryModel(admin.ModelAdmin):
    list_display = ['id', 'book', 'book_id']

@admin.register(BookLogs)
class BookLogsModel(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'book_inventry', 'issue_day', 'checkback', 'due_date', 'fees_to_be_added']

@admin.register(BookModel)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_type_id', 'book_name', 'author', 'base_fee', 'current_count', 'no_of_issued']
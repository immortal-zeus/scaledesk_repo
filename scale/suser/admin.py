from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import Usercus , Userchan
User = get_user_model()
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = Usercus
    form = Userchan
    model = User
    list_display = ('email', 'first_name', 'desgination','reports_to','getting_report')
    list_filter = ('email','first_name', 'desgination','reports_to','getting_report')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Position_Status', {'fields':('desgination','reports_to','getting_report')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
        ),
    )
    search_fields = ('email','desgination','reports_to','getting_report')
    ordering = ('email',)


admin.site.register(User,CustomUserAdmin)

admin.site.register(Desgniation)

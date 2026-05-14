from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Salesman

class SalesmanAdmin(UserAdmin):
    model = Salesman
    list_display = ('username', 'email', 'role', 'salesmanName')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('salesmanId', 'salesmanCode' , 'salesmanName', 'salesmanPhoneNumber', 'role', 'onTally')}),
    )

admin.site.register(Salesman, SalesmanAdmin)

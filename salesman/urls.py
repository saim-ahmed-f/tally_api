from django.urls import path

from .views import *

urlpatterns = [
    path('get/all/', salesmen_list, name='salesmen_list'),
    path('get/<uuid:salesman_id>/' , salesman_by_Id , name="Get Salesman By primary key"),
    path("search/<str:search_term>/" , search_by_text , name="Search through fields"),
    path('post/', salesmen_create_update, name='salesmen_create'),
    path('delete/<uuid:salesman_id>/', salesman_delete, name='salesman_delete'),

    #! Login API
    path("login/" , login_view , name="Login with username and password"),

    #! Tally Api's
    path('tally/getAll/', get_salesmen_tally, name='salesmen list tally'),
    path('tally/postSalesman/' , post_salesman_tally , name="Post & update Salesman")    
]

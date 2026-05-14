from django.urls import path

from .views import *

urlpatterns = [
    path('get/all/', customer_list, name='customer_list'),
    path('get/<uuid:customer_id>/', get_by_Id, name='Get Customer by Primary Key'),
    path('get/customercode/<str:customerCode>/' , customer_list_by_Code , name="get Customer with Customer Code"),
    path('get/salesman/<uuid:salesman_id>/', get_by_salesmanId, name='Get Customer by Salesman ID'),
    path('post/', customer_create, name='customer_create'),
    path('<uuid:customer_id>/delete/', customer_delete, name='customer_delete'),

    path('search/<str:search_term>/', search_by_text, name='Get by Search Text'),



    #! Tally Api's
    path('tally/getAll/', get_customers_tally, name='customers Tally'),
    path('tally/postCustomer/' , post_customer_tally , name="Customer Posted by tally"),
]

from django.urls import path

from .views import *

urlpatterns = [

    path('get/all/', voucher_app_list, name='voucher_list'),
    path('get/<uuid:voucherId>/' , get_by_id , name="Get Voucher by Primary Key"),
    path('get/number/<str:voucherNumber>/' , get_by_voucherNumber , name="Get Voucher by Voucher Number"),
    path('post/' , voucher_create_or_update  ,name="Create New or update existing voucher"),

    path('voucherForToday/', voucherNumberForToday, name='voucher_list'),

    path('get/historicRate/' , get_voucher_search_by_cust_Salesman , name="Get Historic Rate of the Customer"),


    #! Tally API's
    path('tally/getAll/', voucher_list, name='voucher_list'),
    path("tally/post/" , create_voucher , name="Create Voucher"),
    path("tally/commit/" , voucher_commit , name="Commit the voucher")
]

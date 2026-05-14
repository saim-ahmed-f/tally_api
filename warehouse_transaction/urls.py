from django.urls import path

from.views import *

urlpatterns = [
    path('get/all/' , warehouseTransaction_list , name="Get Product warehouse wise",),
    path('get/<uuid:warehouseTransaction_id>/' , get_by_id , name="Get warehouse Transaction in primary Key"),

    #! Tally Api's
    path('tally/getAll/' , get_warehouseTransaction_tally , name="Get All The Warehouse Transactions"),
    path('tally/postWarehouseTransaction/' , post_warehouseTransaction_tally , name="Post Warehouse Transactions")
       
]

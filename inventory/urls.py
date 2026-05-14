from django.urls import path

from.views import *

urlpatterns = [
    path('get/all/' , inventoryProductWiseWarehouse , name="Get product wise inventory"),
    path('get/<uuid:productId>/<uuid:warehouseId>/' , get_by_id , name="Get Inventory ID"),
    path("get/<uuid:warehouseId>/" , get_summery_by_warehouseId , name="Aggrigate product by warehouse Id"),

    #! Tally Api's
    # path('tally/getAll/' , get_warehouseTransaction_tally , name="Get All The Warehouse Transactions"),
    # path('tally/postWarehouseTransaction/' , post_warehouseTransaction_tally , name="Post Warehouse Transactions")
       
]

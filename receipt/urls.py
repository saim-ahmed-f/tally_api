from django.urls import path 
from .views import *


urlpatterns = [
 path('get/all/', receipt_app_list, name='List of Receipts'),
    path('get/<uuid:receiptId>/', get_by_id, name='Get Receipt by Primary Key'),
    path('get/<str:voucherId>/', get_by_voucherId, name='Get receipt by voucher ID'),
    path('post/', receipt_create, name='receipt'),
    # path('<uuid:customer_id>/delete/', customer_delete, name='customer_delete'),
   
]

from django.urls import path

from .views import *


urlpatterns = [
    path('get/all/', warehouse_list, name='warehouse_list'),
    path('get/<uuid:warehouse_id>/' , get_by_id , name="Get Warehouse by Primary ID"),        
    path('post/', warehouse_create, name='warehouse_create'),
    path('delete/<uuid:warehouse_id>/', warehouse_delete, name='warehouse_delete'),

    #! Tally Api's
    path('tally/getAll/', get_warehouse_tally, name='Warehouse Tally'),
    path('tally/postWarehouse/' , post_warehouse_tally , name="Warehouse Posted by tally"),


]

from django.urls import path
from .views import *

urlpatterns = [
    path('get/all/', product_list, name='product_list'),
    path('get/<uuid:product_id>/' , get_by_id , name="Gett Product by id"),
    path('post/', product_create, name='product_create'),
    path('delete/<uuid:product_id>/', product_delete, name='product_delete'),

    path('search/<str:search_term>/', search_by_text, name='Get by Search Text'),


    #! Tally Api's
    path('tally/getAll/', get_product_tally, name='product Tally'),
    path('tally/postProduct/' , post_product_tally , name="product Posted by tally"),

]

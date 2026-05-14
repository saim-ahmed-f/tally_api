from django.urls import path

from .views import *

urlpatterns = [
    path('get/all/', voucher_type_list, name='voucher_type_list'),
    # path('voucher-types/create/', voucher_type_create, name='voucher_type_create'),
    # path('voucher-types/<uuid:voucher_type_id>/delete/', views.voucher_type_delete, name='voucher_type_delete'),

]

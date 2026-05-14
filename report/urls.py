from django.urls import path 
from .views import *

urlpatterns = [
        path("reportGenerator/" , reportGenerator , name='Dynamic report by Model,fields,aggrigate and Dates.'),
        path("salesReportByMonth/" , salesReportByMonth , name='Sales Report By Month.'),
    ]

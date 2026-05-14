"""
URL configuration for tally_api_testing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include

from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('salesman/', include("salesman.urls")),
    path('customer/', include("customer.urls")),
    path('product/', include("product.urls")),
    path('voucherType/', include("voucher_type.urls")),
    path('voucher/', include("voucher.urls")),
    path('voucherTransaction/', include("voucher_transaction.urls")),
    path('warehouse/', include("warehouse.urls")),
    path('warehouseTransaction/', include("warehouse_transaction.urls")),
    path('inventory/', include("inventory.urls")),
    path('receipt/', include("receipt.urls")),
    path("report/" , include("report.urls")),

    #! Auth Token API
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]

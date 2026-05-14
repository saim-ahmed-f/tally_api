from django.shortcuts import render
from django.db.models import Count
from django.db import connection
from django.db.models import Sum

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


# Import Product & Warehouse 
from product.models import Product
from warehouse.models import Warehouse
from warehouse.serializers import WarehouseReadSerializerApp


# Auth Decorator
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App



@api_view(['GET'])
@Auth_decorator_App
def inventory_list(request):
    inventoryObj = Inventory.objects.all()
    serializer = InventorySerializerForApp(inventoryObj, many=True)
    return Response(serializer.data , status=status.HTTP_200_OK)


@api_view(['GET'])
@Auth_decorator_App
def inventoryProductWiseWarehouse(request):
    try:
        all_product = []
        allInventory = Inventory.objects.values('product__productId').annotate(total = Count('product__productId'))
        for i in allInventory:
            allWarehouse = [ WarehouseReadSerializerApp(warehouseObj.warehouse).data for warehouseObj in Inventory.objects.filter(product = i["product__productId"]) ]
            inventoryValue = Inventory.objects.filter(product = i["product__productId"] , warehouse = allWarehouse[0]["warehouseId"])
            result = InventoryReadSerilaizerApp_PRODUCTWISE(inventoryValue[0]).data
            result['warehouse'] = allWarehouse
            all_product.append(result)
            
        return Response(all_product , status= status.HTTP_200_OK)
    except Exception as error:
        return Response({'status' : str(error)} , status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@Auth_decorator_App
def get_by_id(request , productId , warehouseId):
    inventoryObj = Inventory.objects.get(product=productId , warehouse = warehouseId)
    serializer = InventorySerializerForApp(inventoryObj)
    return Response(serializer.data , status=status.HTTP_200_OK)


@Auth_decorator_App
@api_view(['GET'])
def get_summery_by_warehouseId(request , warehouseId):
    try:

        inventory_summary = (
            Inventory.objects
            .filter(warehouse__warehouseId=warehouseId)
            .values('product__productId', 'product__productName')  # Group by product
            .annotate(total_quantity=Sum('quantity'))              # Sum quantity
            .order_by('-total_quantity')                           # Descending order
        )

        return Response(inventory_summary , status=status.HTTP_200_OK)
    except Exception:
        return Response({"Status" : False , "detail" : "Something went wrong!!!"} , status=status.HTTP_400_BAD_REQUEST)

#!  Tally Warehouse Transaction API

# @api_view(["GET"])
# def get_warehouseTransaction_tally(request):
#     warehouseTransaction_objs = Inventory.objects.filter(onTally = False)
#     for wareTrans in warehouseTransaction_objs:
#         wareTrans.onTally = True
#         wareTrans.save()
#     serializer = WarehouseTransactionReadSerializerTally(warehouseTransaction_objs , many = True)
#     return Response({"warehouseTransactions": serializer.data})

# @api_view(["POST"])
# def post_warehouseTransaction_tally(request):
#     warehouseTrans_data = request.data.get("warehouseTransactions")

#     if not warehouseTrans_data or not isinstance(warehouseTrans_data, list):
#         return Response({'error': 'Expected "Warehouse Transaction" to be a list of objects.'},status=status.HTTP_400_BAD_REQUEST)

#     response_data = []

#     for item in warehouseTrans_data:
#         warehouseTransaction_Id = item.get('warehouseTransactionId')


#         if not warehouseTransaction_Id:
#             return Response({'error': 'Expected "Warehouse" ID.'},status=status.HTTP_400_BAD_REQUEST)

#         product_Id = item.get('product')
#         warehouse_Id = item.get('warehouse')

#         if not product_Id or not warehouse_Id:
#             return Response({'error': 'Expected "Product and Warehouse" valid ID.'},status=status.HTTP_400_BAD_REQUEST)
#         else:
#             try:
#                 productObj = Product.objects.get(productId = product_Id)
#                 warehouseObj = Warehouse.objects.get(warehouseId = warehouse_Id)
#             except Warehouse.DoesNotExist:
#                     return Response({'error': 'Warehouse Does not exist in database.'},status=status.HTTP_400_BAD_REQUEST)
#             except Product.DoesNotExist:
#                     return Response({'error': 'Product Does not exist in database.'},status=status.HTTP_400_BAD_REQUEST)



#         warehouseTransactionobjs, created = warehouseTransaction.objects.update_or_create(
#             warehouseTransactionId = warehouseTransaction_Id,
#             defaults={
#                 'product': productObj,
#                 'warehouse' : warehouseObj,
#                 'rate' : item.get('rate'),
#                 'quantity' : item.get('quantity')
#             }
#         )


#         serializer = WarehouseTransactionWriteSerializerTally(warehouseTransactionobjs)

#         response_data.append(serializer.data)
    
#     return Response(response_data, status=status.HTTP_201_CREATED)
    


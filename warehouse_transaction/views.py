from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import warehouseTransaction
from .serializers import *


# Import Product & Warehouse 
from product.models import Product
from warehouse.models import Warehouse


# Auth Decorator
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App



@Auth_decorator_App
@api_view(['GET'])
def warehouseTransaction_list(request):
    warehousesTrans = warehouseTransaction.objects.all()
    serializer = WarehouseTransactionReadSerializerApp(warehousesTrans, many=True)
    return Response(serializer.data , status=status.HTTP_200_OK)

@Auth_decorator_App
@api_view(['GET'])
def get_by_id(request , warehouseTransaction_id):
    warehousesTrans = warehouseTransaction.objects.get(pk = warehouseTransaction_id)
    serializer = WarehouseTransactionReadSerializerApp(warehousesTrans)
    return Response(serializer.data , status=status.HTTP_200_OK)






#!  Tally Warehouse Transaction API

@api_view(["GET"])
def get_warehouseTransaction_tally(request):
    warehouseTransaction_objs = warehouseTransaction.objects.filter(onTally = False)
    for wareTrans in warehouseTransaction_objs:
        wareTrans.onTally = True
        wareTrans.save()
    serializer = WarehouseTransactionReadSerializerTally(warehouseTransaction_objs , many = True)
    return Response({"warehouseTransactions": serializer.data})

@api_view(["POST"])
def post_warehouseTransaction_tally(request):
    warehouseTrans_data = request.data.get("warehouseTransactions")

    if not warehouseTrans_data or not isinstance(warehouseTrans_data, list):
        return Response({'error': 'Expected "Warehouse Transaction" to be a list of objects.'},status=status.HTTP_400_BAD_REQUEST)

    response_data = []

    for item in warehouseTrans_data:
        warehouseTransaction_Id = item.get('warehouseTransactionId')


        if not warehouseTransaction_Id:
            return Response({'error': 'Expected "Warehouse" ID.'},status=status.HTTP_400_BAD_REQUEST)

        product_Id = item.get('product')
        warehouse_Id = item.get('warehouse')

        if not product_Id or not warehouse_Id:
            return Response({'error': 'Expected "Product and Warehouse" valid ID.'},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                productObj = Product.objects.get(productId = product_Id)
                warehouseObj = Warehouse.objects.get(warehouseId = warehouse_Id)
            except Warehouse.DoesNotExist:
                    return Response({'error': 'Warehouse Does not exist in database.'},status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                    return Response({'error': 'Product Does not exist in database.'},status=status.HTTP_400_BAD_REQUEST)



        warehouseTransactionobjs, created = warehouseTransaction.objects.update_or_create(
            warehouseTransactionId = warehouseTransaction_Id,
            defaults={
                'product': productObj,
                'warehouse' : warehouseObj,
                'rate' : item.get('rate'),
                'quantity' : item.get('quantity')
            }
        )


        serializer = WarehouseTransactionWriteSerializerTally(warehouseTransactionobjs)

        response_data.append(serializer.data)
    
    return Response(response_data, status=status.HTTP_201_CREATED)
    


# warehouse/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Warehouse
from .serializers import *

import uuid


# Auth Decorator
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App

@Auth_decorator_App
@api_view(['GET'])
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    serializer = WarehouseReadSerializerApp(warehouses, many=True)
    return Response(serializer.data)

@Auth_decorator_App
@api_view(['GET'])
def get_by_id(request , warehouse_id):
    warehouses = Warehouse.objects.get(pk = warehouse_id)
    serializer = WarehouseReadSerializerApp(warehouses)
    return Response(serializer.data)


@Auth_decorator_App
@api_view(['POST'])
def warehouse_create(request):
    lookup_id = request.data.get('warehouseId')  # Primary Key field Name

    if lookup_id:
        try:
            # Required Model
            objToUpdate = Warehouse.objects.get(pk=lookup_id)
            # Required Serializer
            serializer = WarehouseWriteSerializerApp(objToUpdate, data=request.data, partial=True)
        # Add Model for does not exist
        except Warehouse.DoesNotExist:
            # Required Serializer to write if not found
            serializer = WarehouseWriteSerializerApp(data=request.data)
    else:
        # Required Serializer to write if not found
        serializer = WarehouseWriteSerializerApp(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        return Response(WarehouseWriteSerializerApp(instance).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@Auth_decorator_App
@api_view(['DELETE'])
def warehouse_delete(request, warehouse_id):
    try:
        warehouse = Warehouse.objects.get(WarehouseId=warehouse_id)
    except Warehouse.DoesNotExist:
        return Response({'error': 'Warehouse not found'}, status=status.HTTP_404_NOT_FOUND)
    warehouse.delete()
    return Response({'message': 'Warehouse deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#!  Tally Warehouse API

@api_view(["GET"])
def get_warehouse_tally(request):
    warehouse_objs = Warehouse.objects.filter(onTally=False)
    for prod in warehouse_objs:
        prod.onTally = True
        prod.save()
    serializer = WarehouseReadSerializerTally(warehouse_objs, many=True)
    return Response({"warehouses": serializer.data})


@api_view(["POST"])
def post_warehouse_tally(request):

    warehouse_data = request.data.get("warehouses")

    if not warehouse_data or not isinstance(warehouse_data, list):
        return Response({'error': 'Expected "Warehouse" to be a list of objects.'},status=status.HTTP_400_BAD_REQUEST)

    response_data = []

    for item in warehouse_data:
        warehouse_id = item.get('warehouseId')
        if not warehouse_id:
            return Response({'error': 'Expected "Warehouse" ID.'},status=status.HTTP_400_BAD_REQUEST)


        warehouse, created = Warehouse.objects.update_or_create(
            warehouseId=warehouse_id,
            defaults={
                'warehouseName': item.get('warehouseName'),
            }
        )


        serializer = WarehouseWriteSerializerTally(warehouse)

        response_data.append(serializer.data)
    
    return Response(response_data, status=status.HTTP_201_CREATED)
    


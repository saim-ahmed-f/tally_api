# warehouse/serializers.py

from rest_framework import serializers
from .models import Warehouse
# from warehouse_transaction.serializers import WarehouseTransactionSerializer

# class WarehouseSerializer(serializers.ModelSerializer):
#     transactions = WarehouseTransactionSerializer(source='warehouseTransaction_warehouse', many=True, read_only=True)
#     class Meta:
#         model = Warehouse
#         fields = [
#             'WarehouseId',
#             'warehouseName',
#             'onTally',
#             'transactions'
#         ]


#! APP Serializer's

class WarehouseReadSerializerApp(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['warehouseId','warehouseName' , 'onTally' ,'created_on' , 'updated_on']

class WarehouseWriteSerializerApp(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['warehouseId','warehouseName']


#? Voucher & Tally Serializer
class WarehouseSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['warehouseId','warehouseName']





#! Tally Serializer

class WarehouseReadSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["warehouseId" , "warehouseName"]
    

class WarehouseWriteSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["warehouseId" , "warehouseName"]



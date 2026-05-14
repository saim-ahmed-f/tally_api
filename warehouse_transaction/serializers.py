from rest_framework import serializers
from .models import warehouseTransaction
from product.models import Product
from warehouse.models import Warehouse
from voucher.models import Voucher

from product.serializers import *
from warehouse.serializers import WarehouseWriteSerializerApp
from voucher.serializers import VoucherWriteSerilaizerApp



class WarehouseTransactionSerializer(serializers.ModelSerializer):
    product = ProductReadSerializerAPP(read_only=True)

    class Meta:
        model = warehouseTransaction
        fields = [
            'warehouseTransactionId',
            'product',
            'quantity',
        ]

#! READ
class WarehouseTransactionReadSerializerApp(serializers.ModelSerializer):
    product = ProductReadSerializerAPP(read_only=True)
    warehouse = serializers.SerializerMethodField()
    

    class Meta:
        model = warehouseTransaction
        fields = [
            'warehouseTransactionId',
            'voucher',
            'warehouse',
            'product',
            'quantity',
        ]

    def get_warehouse(self, obj):
        from warehouse.serializers import WarehouseReadSerializerApp  # lazy import here
        return WarehouseReadSerializerApp(obj.warehouse).data
    

class WarehouseTransactionWriteSerializerApp(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    voucher = serializers.PrimaryKeyRelatedField(queryset=Voucher.objects.all())
    class Meta:
        model = warehouseTransaction
        fields = [
            # 'warehouseTransactionId',
            'voucher',
            'warehouse',
            'product',
            'quantity',
        ]


#! Tally Serializer

class WarehouseTransactionReadSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = warehouseTransaction
        fields = ["warehouseTransactionId" , "product" , "warehouse" , "quantity"]


class WarehouseTransactionWriteSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = warehouseTransaction
        fields = ["warehouseTransactionId" , "product" , "warehouse" , "quantity"]

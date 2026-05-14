from rest_framework import serializers
from .models import *
from product.models import Product
from warehouse.models import Warehouse
from product.serializers import *

from warehouse.serializers import WarehouseReadSerializerApp

#! APP SERIALIZER's

class InventorySerializer(serializers.ModelSerializer):
    product = ProductReadSerializerAPP(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            'inventoryId',
            'product',
            'rate',
            'quantity',
            'created_on',
            'updated_on'
        ]


class InventoryReadSerilaizerApp_PRODUCTWISE(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            'product',
            'rate',
            'quantity',
            'created_on',
            'updated_on'
        ]


class InventorySerializerForApp(serializers.ModelSerializer):
    product = ProductReadSerializerAPP(read_only=True)
    warehouse = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            'inventoryId',
            'warehouse',
            'product',
            'rate',
            'quantity',
            'created_on',
            'updated_on'
        ]

    def get_warehouse(self, obj):
        from warehouse.serializers import WarehouseReadSerializerApp
        return WarehouseReadSerializerApp(obj.warehouse).data


#! WRITE
class InventoryWriteSerializerApp(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    class Meta:
        model = Inventory
        fields = [
            # 'inventoryId',
            'product',
            'warehouse',
            'rate',
            'quantity',
            'created_on',
            'updated_on'
        ]


# voucher_transaction/serializers.py

from rest_framework import serializers
from .models import VoucherTransaction
from product.models import Product
from warehouse.models import Warehouse
from voucher.models import Voucher
from product.serializers import *
from warehouse.serializers import WarehouseReadSerializerApp , WarehouseSerializerTally



#! APP Serializer's

#! READ
class VoucherTransactionReadSerializerApp(serializers.ModelSerializer):
    product = ProductReadSerializerAPP(read_only=True)
    warehouse = WarehouseReadSerializerApp(read_only=True)
    class Meta:
        model = VoucherTransaction
        fields = [
            'voucherTransactionId',
            'product',
            'warehouse',
            'rate',
            'quantity',
            'amount',
            'vatPercentage',
            'vatAmount',
            'TotalAmount',
            'created_on',
            'updated_on'
        ]


#! WRITE
class VoucherTransactionWriteSerializerApp(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    voucher = serializers.PrimaryKeyRelatedField(queryset=Voucher.objects.all())
    class Meta:
        model = VoucherTransaction
        fields = [
            # 'voucherTransactionId',
            'voucher',
            'product',
            'warehouse',
            'rate',
            'quantity',
            'amount',
            'vatPercentage',
            'vatAmount',
            'TotalAmount',
        ]





class VoucherTransactionSerializer(serializers.ModelSerializer):
    product = ProductReadSerializerAPP(read_only=True)
    warehouse = WarehouseReadSerializerApp(read_only=True)
    

    class Meta:
        model = VoucherTransaction
        fields = [
            'voucherTransactionId',
            'product',
            'warehouse',
            'rate',
            'quantity',
            'amount',
            'vatPercentage',
            'vatAmount',
            'TotalAmount'
        ]

#? Tally & Voucher Serializer

class VoucherTransactionSerializerForVoucher_Tally(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all())
    

    class Meta:
        model = VoucherTransaction
        fields = [
            'voucherTransactionId',
            'product',
            'warehouse',
            'rate',
            'quantity',
            'amount',
            'vatPercentage',
            'vatAmount',
            'TotalAmount'
        ]

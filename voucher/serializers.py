# voucher/serializers.py
from decimal import Decimal
from rest_framework import serializers
from .models import Voucher
from warehouse.models import Warehouse
from product.models import Product
from salesman.models import Salesman
from customer.models import Customer
from voucher_type.models import VoucherType
from voucher_transaction.models import VoucherTransaction

from warehouse_transaction.models import warehouseTransaction

from voucher_transaction.serializers import *


from salesman.serializers import  *
from customer.serializers import *
from voucher_type.serializers import VoucherTypeSerializerForVoucher
from receipt.serializers import *

#! APP Serializer's


#! READ
class VoucherReadSerilaizerApp(serializers.ModelSerializer):
    voucherDate = serializers.DateField(format="%Y-%m-%d", read_only=True)
    salesman = SalesmanReadSerializerApp(read_only=True)
    customer = CustomerReadSerializerApp(read_only=True)
    voucherType = VoucherTypeSerializerForVoucher(read_only=True)
    allInventory = VoucherTransactionReadSerializerApp(many=True , read_only=True)
    receipt = ReceiptReadSerializerAPP(source='receipt_voucher' , many=True , read_only = True)
    class Meta:
        model = Voucher
        fields = [
            'voucherId',
            'voucherDate',
            'voucherNumber',
            'voucherRemark',
            'salesman',
            'customer',
            'voucherType',
            'allInventory',
            'receipt',
            'onTally',
            'created_on',
            'updated_on'
        ]


#! WRITE

class VoucherWriteSerilaizerApp(serializers.ModelSerializer):
    voucherRemark = serializers.CharField(required=False, allow_blank=True)
    voucherDate = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    class Meta:
        model = Voucher
        fields = [
            'voucherId',
            'voucherDate',
            'voucherNumber',
            'voucherRemark',
            'salesman',
            'customer',
            'voucherType',
        ]









#? Tally & Voucher Serializer
class VoucherSerializerForTally(serializers.ModelSerializer):
    salesman = SalesmanSerializerForVoucher(read_only=True)
    customer = TallyCustomerSerializer(read_only=True)
    voucherType = VoucherTypeSerializerForVoucher(read_only=True)
    
    allInventory = VoucherTransactionSerializerForVoucher_Tally(many=True, read_only=True)
    

    class Meta:
        model = Voucher
        fields = [
            'voucherId',
            'voucherDate',
            'voucherNumber',
            'voucherRemark',
            'salesman',
            'customer',
            'voucherType',
            'allInventory',
            # 'onTally',
        ]

    



#? WRITE 

class VoucherWriteSerializerForTally(serializers.ModelSerializer):
    allInventory = serializers.ListField() #VoucherTransactionSerializer(many=True)


    salesman = serializers.DictField()
    customer = serializers.DictField()
    

    # Accept nested dict for voucherType, handle manually in create()
    voucherType = serializers.DictField()

    class Meta:
        model = Voucher
        fields = [
            'voucherId',
            'voucherDate',
            'voucherNumber',
            'voucherRemark',
            'salesman',
            'customer',
            'voucherType',
            'allInventory',
            'receipts',
            'onTally'
        ]

    def create(self, validated_data):
        inventory_data = validated_data.pop('allInventory')
        receipts_data = validated_data.pop('receipts', [])

        # Extract voucherType from nested data
        voucher_type_data = validated_data.pop('voucherType')
        voucher_type_name = voucher_type_data.get('voucherName')


        # Extracting Salesman Data from nested Data
        salesman_data = validated_data.pop("salesman")
        salesmanId = salesman_data.get('salesmanId')

        # Extracting Customer Data from nested Data
        customerId_data = validated_data.pop('customer')
        customerId = customerId_data.get('customerId')
        
        try:
            voucher_type_obj = VoucherType.objects.get(voucherName__iexact=voucher_type_name)
        except VoucherType.DoesNotExist:
            raise serializers.ValidationError({"voucherType": "Invalid voucher type name."})
        

        try:
            salesman_obj = Salesman.objects.get(salesmanId__iexact=salesmanId)
        except VoucherType.DoesNotExist:
            raise serializers.ValidationError({"voucherType": "Invalid Salesman Id."})
        
        try:
            customer_obj = Customer.objects.get(CustomerId__iexact=customerId)
        except VoucherType.DoesNotExist:
            raise serializers.ValidationError({"voucherType": "Invalid Customer Id."})

        # Now create the voucher
        voucher = Voucher.objects.create(voucherType=voucher_type_obj, salesman = salesman_obj , customer = customer_obj, **validated_data)

        # Create voucher transactions and updating the warehouse Inventory
        for item in inventory_data:
            print(f"\n\n\n\n{item}--------------------------------\n\n\n\n")
            product = Product.objects.get(productId=item.pop('product').get('productId'))
            warehouse = Warehouse.objects.get(WarehouseId=item.pop('warehouse').get('WarehouseId'))

            voucherTrans = VoucherTransaction.objects.create(voucher=voucher,product = product , warehouse = warehouse, **item)
            if voucher_type_name.lower() == 'voucher':
                try:
                    warehouseTrans = warehouseTransaction.objects.get(product = voucherTrans.product , rate = voucherTrans.rate)
                    warehouseTrans.quantity = warehouseTrans.quantity + Decimal(voucherTrans.quantity)
                    warehouseTrans.save()
                except warehouseTransaction.DoesNotExist:
                    warehouseTransaction.objects.create(
                    product=voucherTrans.product,
                    warehouse=voucherTrans.warehouse,
                    rate=Decimal(voucherTrans.rate),
                    quantity=Decimal(voucherTrans.quantity)
                    )



       

        return voucher

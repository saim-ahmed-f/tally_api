

from rest_framework import serializers
from .models import Receipt

from voucher.models import Voucher

#! APP Serializer's

class ReceiptReadSerializerAPP(serializers.ModelSerializer):
    paymentDate = serializers.DateField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Receipt
        fields = ["receiptId" , "paymentMode" , "paymentStatus" , "voucher" , "paymentDate" , "paymentAmount" , "onTally" , "created_on" , "updated_on"]


class ReceiptWriteSerializerAPP(serializers.ModelSerializer):
    paymentDate = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    voucher = serializers.PrimaryKeyRelatedField(queryset = Voucher.objects.all())
    class Meta:
        model = Receipt
        fields = ["receiptId" , "paymentMode" , "paymentStatus" , "voucher" , "paymentDate" , "paymentAmount" ]
# voucher/serializers.py

from rest_framework import serializers
from .models import VoucherType

class VoucherTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherType
        fields = ['voucherName']


#?  Voucher & Tally Serializer

class VoucherTypeSerializerForVoucher(serializers.ModelSerializer):
    class Meta:
        model = VoucherType
        fields = ['voucherName']


#! Tally Serializer

class VoucherTypeReadSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = VoucherType
        fields= "__all__"

class VoucherTypeWriteSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = VoucherType
        fields= "__all__"
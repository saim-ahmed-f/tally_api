# product/serializers.py

from rest_framework import serializers
from .models import Product

#! APP Serializer's

class ProductReadSerializerAPP(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'baseUnit', 'productCode' , 'productName' , 'onTally' , 'created_on' , 'updated_on']

class ProductWriteSerializerAPP(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'baseUnit', 'productCode' , 'productName']


#! Tally Serializer

class ProductReadSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'productName', 'baseUnit']


class ProductWriteSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'productName', 'baseUnit']

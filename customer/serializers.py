# customer/serializers.py

from rest_framework import serializers
from .models import Customer


#! APP Serilaizer's

class CustomerReadSerializerApp(serializers.ModelSerializer):
    salesman = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ['customerId' , 'customerCode' , 'customerName' , 'salesman' , 'onTally' , 'created_on' , 'updated_on']
    
    def get_salesman(self, obj):
        from salesman.serializers import SalesmanReadSerializerApp  # Lazy import
        return SalesmanReadSerializerApp(obj.salesman).data

class CustomerWriteSerializerApp(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customerId' , 'customerCode' , 'customerName' , 'salesman' , 'onTally' , 'created_on' , 'updated_on']





#! TALLY APIS SERIALIZER
class CustomerReadSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customerId' ,'customerName' , 'salesman']

class CustomerWriteSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customerId', 'customerName', 'salesman']



#? Tally & Voucher Serializer 
class TallyCustomerSerializer(serializers.ModelSerializer):
    customerName = serializers.CharField(source='customerName')
    customerId = serializers.CharField(source = 'customerId')

    class Meta:
        model = Customer
        fields = ['customerId' ,'customerName']



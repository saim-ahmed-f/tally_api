from rest_framework import serializers
from .models import Salesman
from customer.models import Customer  # Import the Customer model
from customer.serializers import CustomerReadSerializerTally , CustomerReadSerializerApp


#! APP Serializer's
class SalesmanWriteSerializerApp(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=True)

    class Meta:
        model = Salesman
        fields = [
            'salesmanId',
            'salesmanCode',
            'salesmanName',
            'salesmanPhoneNumber',
            'role',
            'username',
            'password',
            # 'updated_on',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Salesman(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class SalesmanReadSerializerApp(serializers.ModelSerializer):
    # customers = CustomerReadSerializerApp(many=True, read_only=True)

    class Meta:
        model = Salesman
        fields = [
            'salesmanId',
            'salesmanName',
            'salesmanCode',
            'salesmanPhoneNumber',
            'role',
            # 'customers',
            'onTally',
            'created_on',
            'updated_on'
        ]

## Serializer for Customer Model

class SalesmanWriteSerializerApp_CUSTOMER(serializers.ModelSerializer):
    class Meta:
        model = Salesman
        fields = ['salesmanId' , 'salesmanName']



#! Tally Serializer

class SalesmanReadSerializerTally(serializers.ModelSerializer):
    customerObj = CustomerReadSerializerTally(many=True , read_only = True)
    class Meta:
        model = Salesman
        fields = ['salesmanId', 'salesmanGUID' , 'salesmanName' , 'salesmanPhoneNumber' , 'customerObj' , 'created_on' , 'updated_on']

class SalesmanWriteSerializerTally(serializers.ModelSerializer):
    class Meta:
        model = Salesman
        fields = ['salesmanId' , 'salesmanName' , 'salesmanPhoneNumber' , 'updated_on']

    

# ? Customer serializer
class CustomerSerializer_tally(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['customerId' , 'customerName' , 'onTally']


class SalesmanSerializer(serializers.ModelSerializer):
    
    customerName = CustomerSerializer_tally(source='customers', many=True)

    class Meta:
        model = Salesman
        fields = ['salesmanId', 'salesmanName' , 'customerName' , 'onTally']


#? Salesman Serializer for Voucher

class SalesmanSerializerForVoucher(serializers.ModelSerializer):
    salesmanName = serializers.CharField()
    salesmanGUID = serializers.CharField()
    salesmanCode = serializers.CharField()
    # Use the nested serializer here
    # customerName = CustomerSerializer_tally(source='customers', many=True)

    class Meta:
        model = Salesman
        fields = ['salesmanId' , 'salesmanGUID' , 'salesmanCode', 'salesmanName']


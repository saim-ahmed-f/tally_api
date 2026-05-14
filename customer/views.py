from django.db.models import Q
from django.shortcuts import render
from .models import Customer
from .serializers import *
# Create your views here.

from salesman.models import Salesman

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Auth Decorator
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App



#! APP Customer API

# GET all customers
@Auth_decorator_App
@api_view(['GET'])
def customer_list(request):
    customers = Customer.objects.all()
    serializer = CustomerReadSerializerApp(customers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def customer_list_by_Code(request, customerCode):
    # Filter customers where customerCode starts with the provided parameter
    customers = Customer.objects.filter(customerCode__startswith=customerCode)
    
    # Serialize the filtered customers
    serializer = CustomerReadSerializerApp(customers, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def search_by_text(request , search_term):
    # search_term = request.GET.get('search', '')  # Get the search term from query params

    # Define the fields you want to search
    fields_to_search = [
        'customerName', 'customerCode',
    ]

    # Build the Q object for dynamic filtering
    query = Q()  # Start with an empty query

    for field in fields_to_search:
        query |= Q(**{f"{field}__startswith": search_term})

    # Perform the query using the Q object
    listOfFilterObj = Customer.objects.filter(query)

    # Serialize the results
    serializer = CustomerReadSerializerApp(listOfFilterObj, many=True)

    return Response(serializer.data)


@Auth_decorator_App
@api_view(['GET'])
def get_by_Id(request , customer_id):
    customers = Customer.objects.get(pk=customer_id)
    serializer = CustomerReadSerializerApp(customers)
    return Response(serializer.data)

@Auth_decorator_App
@api_view(['GET'])
def get_by_salesmanId(request, salesman_id):
    customers = Customer.objects.filter(salesman__salesmanId=salesman_id)
    serializer = CustomerReadSerializerApp(customers, many=True)
    return Response(serializer.data)


# POST create a new customer
@Auth_decorator_App
@api_view(['POST'])
def customer_create(request):
    lookup_id = request.data.get('customerId')  # Primary Key field Name

    if lookup_id:
        try:
            # Required Model
            objToUpdate = Customer.objects.get(pk=lookup_id)
            # Required Serializer
            serializer = CustomerWriteSerializerApp(objToUpdate, data=request.data, partial=True)
        # Add Model for does not exist
        except Customer.DoesNotExist:
            # Required Serializer to write if not found
            serializer = CustomerWriteSerializerApp(data=request.data)
    else:
        # Required Serializer to write if not found
        serializer = CustomerWriteSerializerApp(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        return Response(CustomerWriteSerializerApp(instance).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE customer by UUID
@Auth_decorator_App
@api_view(['DELETE'])
def customer_delete(request, customer_id):
    try:
        customer = Customer.objects.get(CustomerId=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    
    customer.delete()
    return Response({'message': 'Customer deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#! Tally Customer API

@api_view(['GET'])
def get_customers_tally(request):
    customers = Customer.objects.filter(onTally=False)
    for cust in customers:
        cust.onTally = True
        cust.save()
    serializer = CustomerReadSerializerTally(customers, many=True)
    return Response({"customers": serializer.data})

@api_view(['POST'])
def post_customer_tally(request):

    customer_data = request.data.get("customers")

    if not customer_data or not isinstance(customer_data, list):
        return Response({'error': 'Expected "customer" to be a list of objects.'},status=status.HTTP_400_BAD_REQUEST)

    response_data = []

    for item in customer_data:
        customer_id = item.get('customerId')
        if not customer_id:
            return Response({'error': 'Expected "Customer" valid ID.'},status=status.HTTP_400_BAD_REQUEST)

        if not  item.get('salesman'):
            return Response({'error': 'Expected "Salesman" valid ID.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            salesmanObj = Salesman.objects.get(salesmanId = item.get('salesman'))
            if not salesmanObj or not isinstance(salesmanObj , Salesman):
                return Response({'error': 'Expected "Salesman" valid ID.'},status=status.HTTP_400_BAD_REQUEST)
        except Salesman.DoesNotExist:
                return Response({'error': '"Salesman" does not exist in database.'},status=status.HTTP_400_BAD_REQUEST)


        customer, created = Customer.objects.update_or_create(
            customerId=customer_id,
            defaults={
                'customerName': item.get('customerName'),
                'salesman': salesmanObj,
            }
        )


        serializer = CustomerWriteSerializerTally(customer)
        response_data.append(serializer.data)
    
    return Response(response_data, status=status.HTTP_201_CREATED)
    
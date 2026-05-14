# product/views.py
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import *


# Auth Decorator
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App


@api_view(['GET'])
@Auth_decorator_App
def product_list(request):
    products = Product.objects.all()
    serializer = ProductReadSerializerAPP(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@Auth_decorator_App
def get_by_id(request , product_id):
    products = Product.objects.get(pk=product_id)
    serializer = ProductReadSerializerAPP(products)
    return Response(serializer.data)

@api_view(['GET'])
def search_by_text(request , search_term):
    # search_term = request.GET.get('search', '')  # Get the search term from query params

    # Define the fields you want to search
    fields_to_search = [
        'productName', 'productCode',
    ]

    # Build the Q object for dynamic filtering
    query = Q()  # Start with an empty query

    for field in fields_to_search:
        query |= Q(**{f"{field}__startswith": search_term})

    # Perform the query using the Q object
    listOfFilterObj = Product.objects.filter(query)

    # Serialize the results
    serializer = ProductReadSerializerAPP(listOfFilterObj, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@Auth_decorator_App
def product_create(request):
    lookup_id = request.data.get('productId')  # Primary Key field Name

    if lookup_id:
        try:
            # Required Model
            objToUpdate = Product.objects.get(pk=lookup_id)
            # Required Serializer
            serializer = ProductWriteSerializerAPP(objToUpdate, data=request.data, partial=True)
        # Add Model for does not exist
        except Product.DoesNotExist:
            # Required Serializer to write if not found
            serializer = ProductWriteSerializerAPP(data=request.data)
    else:
        # Required Serializer to write if not found
        serializer = ProductWriteSerializerAPP(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        return Response(ProductWriteSerializerAPP(instance).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@Auth_decorator_App
def product_delete(request, product_id):
    try:
        product = Product.objects.get(productId=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#! Tally Product API

@api_view(["GET"])
def get_product_tally(request):
    products_objs = Product.objects.filter(onTally=False)
    for prod in products_objs:
        prod.onTally = True
        prod.save()
    serializer = ProductReadSerializerTally(products_objs , many=True)
    return Response({"products": serializer.data})


@api_view(["POST"])
def post_product_tally(request):

    product_data = request.data.get("products")

    if not product_data or not isinstance(product_data, list):
        return Response({'error': 'Expected "product" to be a list of objects.'},status=status.HTTP_400_BAD_REQUEST)

    response_data = []

    for item in product_data:
        product_id = item.get('productId')
        if not product_id:
            return Response({'error': 'Expected "Product" ID.'},status=status.HTTP_400_BAD_REQUEST)


        product, created = Product.objects.update_or_create(
            productId=product_id,
            defaults={
                'productName': item.get('productName'),
                'baseUnit': item.get('baseUnit')
            }
        )


        serializer = ProductWriteSerializerTally(product)

        response_data.append(serializer.data)
    
    return Response(response_data, status=status.HTTP_201_CREATED)
    


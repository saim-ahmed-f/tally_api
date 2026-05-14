# salesman/views.py
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Salesman
from .serializers import *


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken


# Auth Deco
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App


#! APP Salesman Api

@Auth_decorator_App
@api_view(['GET'])
def salesmen_list(request):
    salesmen = Salesman.objects.all()
    serializer = SalesmanReadSerializerApp(salesmen, many=True)
    return Response(serializer.data)

@Auth_decorator_App
@api_view(['GET'])
def salesman_by_Id(request , salesman_id):
    salesmenObj = Salesman.objects.get(pk=salesman_id)
    serializeSalesman = SalesmanReadSerializerApp(salesmenObj)
    return Response(serializeSalesman.data , status= status.HTTP_200_OK)

@Auth_decorator_App
@api_view(['GET'])
def search_by_text(request , search_term):
    # search_term = request.GET.get('search', '')  # Get the search term from query params

    # Define the fields you want to search
    fields_to_search = [
        'salesmanName', 'salesmanCode', 'salesmanPhoneNumber'
    ]

    # Build the Q object for dynamic filtering
    query = Q()  # Start with an empty query

    for field in fields_to_search:
        query |= Q(**{f"{field}__startswith": search_term})

    # Perform the query using the Q object
    salesmen = Salesman.objects.filter(query)

    # Serialize the results
    serializer = SalesmanReadSerializerApp(salesmen, many=True)

    return Response(serializer.data)



@api_view(['POST'])
def salesmen_create_update(request):
    lookup_id = request.data.get('salesmanId')  # Primary Key field Name

    if lookup_id:
        try:
            # Required Model
            salesman = Salesman.objects.get(pk=lookup_id)
            # Required Serializer
            serializer = SalesmanWriteSerializerApp(salesman, data=request.data, partial=True)
        except Salesman.DoesNotExist:
            # Required Serializer to write if not found
            serializer = SalesmanWriteSerializerApp(data=request.data)
    else:
        # Required Serializer to write if not found
        serializer = SalesmanWriteSerializerApp(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        return Response(SalesmanWriteSerializerApp(instance).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def salesman_delete(request, salesman_id):
    try:
        salesman = Salesman.objects.get(salesmanId=salesman_id)
    except Salesman.DoesNotExist:
        return Response({'error': 'Salesman not found'}, status=status.HTTP_404_NOT_FOUND)
    salesman.delete()
    return Response({'message': 'Salesman deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



#! LOGIN VIEW's

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'detail': 'Username and password are required'}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response({'detail': 'Invalid credentials'}, status=401)

    access_token = AccessToken.for_user(user)
    userSerialize = SalesmanReadSerializerApp(user)
    return Response({
        'access': str(access_token),
        "salesmanInfo" : userSerialize.data
    })





#! Tally Salesman API

# ? Tally Get all
@api_view(['GET'])
def get_salesmen_tally(request):
    salesmen = Salesman.objects.all()
    # salesmen = Salesman.objects.filter(onTally = False)
    # for sales in salesmen:
    #     sales.onTally = True
    #     sales.save()
    serializer = SalesmanReadSerializerTally(salesmen, many=True)
    return Response({"salesmans": serializer.data})


@api_view(['POST'])
def post_salesman_tally(request):
    salesman_data = request.data.get("salesmans")

    if not salesman_data or not isinstance(salesman_data , list):
        return Response({'error': 'Expected "salesman" to be a list of objects.'}, status=status.HTTP_400_BAD_REQUEST)

    response_data = []

    for item in salesman_data:
        salesman_Id = item.get('salesmanId')
        if not salesman_Id:
            continue

        #? Update or Create Logic
        salesman , created = Salesman.objects.update_or_create(
            salesmanId = salesman_Id,
            defaults={
                'salesmanName' : item.get('salesmanName'),
                "salesmanPhoneNumber" : item.get('salesmanPhoneNumber'),
            }
        )

        serializer = SalesmanWriteSerializerTally(salesman)
        response_data.append(serializer.data)

    return Response(response_data, status=status.HTTP_201_CREATED)
    
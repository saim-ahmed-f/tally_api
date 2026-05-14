from django.shortcuts import render
from .models import Receipt
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App
# Create your views here.

@Auth_decorator_App
@api_view(['GET'])
def receipt_app_list(request):
    receipts = Receipt.objects.all()
    serializer = ReceiptReadSerializerAPP(receipts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@Auth_decorator_App
@api_view(['GET'])
def get_by_id(request , receiptId):
    receipts = Receipt.objects.get(pk = receiptId)
    serializer = ReceiptReadSerializerAPP(receipts)
    return Response(serializer.data, status=status.HTTP_200_OK)

@Auth_decorator_App
@api_view(['GET'])
def get_by_voucherId(request , voucherId):
    receipts = Receipt.objects.get(voucher__voucherId = voucherId)
    serializer = ReceiptReadSerializerAPP(receipts , many =True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@Auth_decorator_App
@api_view(['POST'])
def receipt_create(request):
    lookup_id = request.data.get('receiptId')  # Primary Key field Name

    if lookup_id:
        try:
            # Required Model
            objToUpdate = Receipt.objects.get(pk=lookup_id)
            # Required Serializer
            serializer = ReceiptWriteSerializerAPP(objToUpdate, data=request.data, partial=True)
        # Add Model for does not exist
        except Receipt.DoesNotExist:
            # Required Serializer to write if not found
            serializer = ReceiptWriteSerializerAPP(data=request.data)
    else:
        # Required Serializer to write if not found
        serializer = ReceiptWriteSerializerAPP(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        return Response(ReceiptWriteSerializerAPP(instance).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


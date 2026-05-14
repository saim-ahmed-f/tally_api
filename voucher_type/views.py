from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .serializers import VoucherTypeSerializer
from .models import VoucherType


# Auth Decorator
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App


# GET all voucher types
@Auth_decorator_App
@api_view(['GET'])
def voucher_type_list(request):
    types = VoucherType.objects.all()
    serializer = VoucherTypeSerializer(types, many=True)
    return Response(serializer.data)

# # POST create new voucher type
# @api_view(['POST'])
# def voucher_type_create(request):
#     serializer = VoucherTypeSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # DELETE voucher type by ID
# @api_view(['DELETE'])
# def voucher_type_delete(request, voucher_type_id):
#     try:
#         vt = VoucherType.objects.get(VoucherTypeId=voucher_type_id)
#     except VoucherType.DoesNotExist:
#         return Response({'error': 'VoucherType not found'}, status=status.HTTP_404_NOT_FOUND)

#     vt.delete()
#     return Response({'message': 'VoucherType deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#! Tally Voucher Type API




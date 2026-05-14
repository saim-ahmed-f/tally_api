from django.shortcuts import render
from django.db.models import Q
# voucher/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Voucher
from .serializers import *
from .voucherActions import mainVoucherActions
from django.utils import timezone

# Auth Decorator
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App


#! APP Api's
@Auth_decorator_App
@api_view(['GET'])
def voucher_app_list(request):
    vouchers = Voucher.objects.all()
    serializer = VoucherReadSerilaizerApp(vouchers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@Auth_decorator_App
@api_view(['GET'])
def get_by_id(request,voucherId):
    vouchers = Voucher.objects.get(pk = voucherId)
    serializer = VoucherReadSerilaizerApp(vouchers)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_by_text(request , search_term):
    # Define the fields you want to search
    fields_to_search = [
        'voucherNumber', 
    ]

    # Build the Q object for dynamic filtering
    query = Q()  # Start with an empty query

    for field in fields_to_search:
        query |= Q(**{f"{field}__startswith": search_term})

    # Perform the query using the Q object
    listOfFilterObj = VoucherReadSerilaizerApp.objects.filter(query)

    # Serialize the results
    serializer = VoucherReadSerilaizerApp(listOfFilterObj, many=True)

    return Response(serializer.data)

@Auth_decorator_App
@api_view(['GET'])
def get_by_voucherNumber(request,voucherNumber):
    vouchers = Voucher.objects.get(voucherNumber = voucherNumber)
    serializer = VoucherReadSerilaizerApp(vouchers)
    return Response(serializer.data, status=status.HTTP_200_OK)


@Auth_decorator_App
@api_view(['GET'])
def voucherNumberForToday(request):
    # Get today's date (no time part, just date)
    today = timezone.now().date()  # This gives a date object, e.g., '2025-08-30'

    # Filter vouchers created today
    vouchers = Voucher.objects.filter(created_on__date=today)

    # Serialize the filtered vouchers
    serializer = VoucherReadSerilaizerApp(vouchers, many=True)

    # Return the serialized data
    return Response(serializer.data, status=status.HTTP_200_OK)


@Auth_decorator_App
@api_view(['POST'])
def voucher_create_or_update(request):
    voucherId = request.data.get('voucherId')
    voucherType = request.data.get('voucherType')
    voucherNumber = request.data.get('voucherNumber')
    allInventory = request.data.get('allInventory')
    allReceipts = list(request.data.get('receipt'))
    del request.data['allInventory']
    del request.data['receipt']

    if voucherId and voucherType and voucherNumber:
        serializer = VoucherWriteSerilaizerApp(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serilizer_data = []
            for data in allInventory:
                result = mainVoucherActions(voucherType , voucherId , data)
                if result['status']:
                    serilizer_data.append(result)
                else:
                    Voucher.objects.get(pk=serializer.data['voucherId']).delete()
                    return Response({"status": False,"errors": "Wrong Data"}, status=status.HTTP_400_BAD_REQUEST)


            serialized_receipt = []
            try:
                # ✅ First loop: validate and store the serializers
                for receipt in allReceipts:
                    reciptSerialize = ReceiptWriteSerializerAPP(data=receipt)
                    if reciptSerialize.is_valid():
                        serialized_receipt.append(reciptSerialize)
                    else:
                        return Response({
                            "status": False,
                            "errors": reciptSerialize.errors
                        }, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({
                    "status": False,
                    "errors": str(e) or "Wrong Data"
                }, status=status.HTTP_400_BAD_REQUEST)




            # SAVING ALL DATA

            for save_serliazer in serilizer_data:
                save_serliazer['voucherTrans'].save()
                save_serliazer['warehouseTrans'].save()

                if save_serliazer['inventory_entry_avail'] == True and save_serliazer['invetoryTrans'].quantity <= 0:
                    save_serliazer['invetoryTrans'].delete()
                else:
                    save_serliazer['invetoryTrans'].save()

            # ✅ Second loop: save all validated receipts
            for saveRecipt in serialized_receipt:
                saveRecipt.save()
            

                    

            return Response({"status" : True} , status=status.HTTP_201_CREATED)
        else:
            return Response({"status": False,"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"status" : "Please provide the voucherId"} , status=status.HTTP_400_BAD_REQUEST)


#! Tally API

@api_view(['GET'])
def voucher_list(request):
    # vouchers = Voucher.objects.all()
    
    # Filter voucher in on tally = false
    vouchers = Voucher.objects.filter(onTally=False)
    # for i in vouchers:
    #     i.onTally = True
    #     i.save()

    serializer = VoucherSerializerForTally(vouchers, many=True)
    return Response({"voucher": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_voucher(request):
    serializer = VoucherWriteSerializerForTally(data=request.data)
    if serializer.is_valid():
        voucher = serializer.save()
        return Response({"voucherId": str(voucher.voucherId)}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def voucher_commit(request):
    completed = []
    try:
        for data in list(request.data["voucherNumber"]):
            v = Voucher.objects.get(pk = data)
            v.onTally = True
            v.save()
            completed.append(data)
    except Exception:
        for data_back in completed:
            v = Voucher.objects.get(pk = data_back)
            v.onTally = False
            v.save()
        return Response({"status" : False},status=status.HTTP_400_BAD_REQUEST)
    return Response({"status" : True}, status=status.HTTP_200_OK)
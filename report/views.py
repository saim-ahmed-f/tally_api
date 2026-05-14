from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
from tally_api_testing.Auth.auth_decorator import Auth_decorator_App
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from voucher_transaction.models import VoucherTransaction  # Adjust if needed


# Database Connector
from django.db import connection



#! Sales Report By salesman 

@Auth_decorator_App
@api_view(['GET'])
def reportGenerator(request):
    # groupByTableName = request.GET.get("groupByTableName")
    groupByModel = str(request.GET.get("groupByModel")).lower()
    groupByFeild = str(request.GET.get("groupByFeild")).split(",")
    aggrigateFunc = str(request.GET.get("aggrigateFunc")).lower()
    aggrigateField = str(request.GET.get("aggrigateField")).lower()
    start_date = request.GET.get('startDate')  # format: dd-mm-yyyy
    end_date = request.GET.get('endDate')

    
    #! string for Date Range
    stringForDateFilter = ""
    if start_date and end_date:
        try:
        # Convert to ISO format for SQL (yyyy-mm-dd)
            start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
            end_date = datetime.strptime(end_date, '%d-%m-%Y').date()

            
            if groupByModel == "voucher":
                stringForDateFilter = f"WHERE V.voucherDate BETWEEN {start_date} AND {end_date} "


        except ValueError:
            return Response({"error": "Invalid date format. Use dd-mm-yyyy."}, status=status.HTTP_400_BAD_REQUEST)

    if not groupByFeild or not groupByModel or not aggrigateFunc or not aggrigateField :
        return Response({"error": "Please provide 'Group By Model Name' , 'Group By Model feild Name' and 'Aggrigate Function' ."}, status=400)



    modelNames = {"product" : "product_product" , "warehouse" : 'warehouse_warehouse' , "customer" : "customer_customer" , "salesman" : "salesman_salesman" , "voucher" : "voucher_voucher"}
    aggFuncNames = ['count' , 'sum']

    if groupByModel not in modelNames.keys():
        return Response({"error": "Please provide a valid Model Name."}, status=status.HTTP_400_BAD_REQUEST)
    if aggrigateFunc not in aggFuncNames:
        return Response({"error": "Please provide a valid Aggrigation Function Name."}, status=status.HTTP_400_BAD_REQUEST)



    #! Aggrigated Line
    stringAggrigateLine = f"{str(aggrigateFunc).upper()}(VT.{aggrigateField}) AS {str(aggrigateFunc).lower()} "


    #! Group by Column String Bulider
    stringGroupByOutputColumn = ""
    stringGroupByLine = ""
    count =0
    for i in list(groupByFeild):
        count += 1
        if len(i.strip()) >0:
            modelAliase = "DM"
            if groupByModel == "voucher":
                modelAliase = "V"
            # For Group By Line 
            stringGroupByLine += f"{modelAliase}.{i}"
            # For Output Column
            stringGroupByOutputColumn += f"{modelAliase}.{i}"
        
        if count != len(groupByFeild):
            stringGroupByLine += ", "
            stringGroupByOutputColumn += ", "
        

    #! Table join for salesman,customer,warehouse
    stringTableJoin = "JOIN "
    if groupByModel not in ["voucher" , "product" , "warehouse"]:
        stringTableJoin += f"{modelNames[groupByModel]} DM ON V.{groupByModel}_id = DM.{groupByModel}Id "
    elif groupByModel in ["product" , "warehouse"]:
        stringTableJoin += f"{modelNames[groupByModel]} DM ON VT.{groupByModel}_id = DM.{groupByModel}Id "
    else:
        stringTableJoin = ""
    

    CUSTOMQUERY = f"""
        SELECT 
        
        
        {stringGroupByOutputColumn}
                       
        ,{stringAggrigateLine}
                       
        FROM voucher_transaction_vouchertransaction VT
        JOIN voucher_voucher V ON VT.voucher_id = V.voucherId
                       
        {stringTableJoin}

        {stringForDateFilter}
                       
        GROUP BY {stringGroupByLine}
                       
        ORDER BY {str(aggrigateFunc).lower()} DESC;
        """


    # print("Generated SQL Query:\n", CUSTOMQUERY)
    try:
        with connection.cursor() as cursor:
            cursor.execute(CUSTOMQUERY)

            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

        return Response(results, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)

@Auth_decorator_App
@api_view(['GET'])
def salesReportByMonth(request):
    try:
        # Set the year you want to report for
        year = datetime.now().year  # You can customize or get from query param

        # Step 1: Get actual sales data grouped by month
        raw_data = VoucherTransaction.objects.filter(
            voucher__voucherType__voucherName='sales',
            voucher__voucherDate__year=year
        ).annotate(
            month=TruncMonth('voucher__voucherDate')
        ).values('month').annotate(
            total_sales=Sum('TotalAmount')
        ).order_by('month')

        # Convert to dictionary for faster lookup
        sales_dict = {
            entry['month'].month: float(entry['total_sales']) for entry in raw_data
        }

        # Step 2: Build full month list with 0 fallback
        result = []
        for month in range(1, 13):
            result.append({
                'year': year,
                'month': month,
                'total_sales': sales_dict.get(month, 0.0)
            })


        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        
        return Response({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


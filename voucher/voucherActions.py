from voucher_transaction.serializers import VoucherTransactionWriteSerializerApp
from warehouse_transaction.serializers import WarehouseTransactionWriteSerializerApp
from inventory.serializers import InventoryWriteSerializerApp
from decimal import Decimal


# INVENTORY IMPORT's
from inventory.models import Inventory


#! SALES VOUCHER
def salesVoucher(voucherId, data):
    data = dict(data)
    voucherTransData = {
        # "voucherTransactionId" : str(uuid4()),
        "voucher" : voucherId,
        "product" : data['product'],
        "warehouse" : data['warehouse'],
        "rate": data["rate"],
        "quantity":  data["quantity"],
        "amount":  data["amount"],
        "vatPercentage":  data["vatPercentage"],
        "vatAmount":  data["vatAmount"],
        "TotalAmount":  data["TotalAmount"]
    }

    warehouseTrans_data = {
        "voucher" : voucherId,
        "warehouse" : data['warehouse'],
        "product" : data['product'],
        "quantity" : Decimal(data["quantity"]) * -1,
    }

    voucherTrans_serialize = VoucherTransactionWriteSerializerApp(data=voucherTransData)

    
    warehouseTrans_serializer = WarehouseTransactionWriteSerializerApp(data=warehouseTrans_data)

    # Inventory
    inventory_entry_available = True
    inventory_serialize_and_Entry = None
    try:
        inventory_serialize_and_Entry = Inventory.objects.get(product = data['product'] , warehouse = data['warehouse'])
        inventory_serialize_and_Entry.quantity -= Decimal(data["quantity"])

    except Inventory.DoesNotExist:
        inventory_entry_available = False
        inventory_data = {
        "product" : data['product'],
        "warehouse" : data['warehouse'],
        "rate" : data["rate"],
        "quantity" : Decimal(data["quantity"]),
        }
        inventory_serialize_and_Entry = InventoryWriteSerializerApp(data = inventory_data)
    
    if voucherTrans_serialize.is_valid() and warehouseTrans_serializer.is_valid() :
        if inventory_entry_available == False and inventory_serialize_and_Entry.is_valid() == False:
            return {"status" : False} 
        return {"status" : True , "voucherTrans" : voucherTrans_serialize , "warehouseTrans" : warehouseTrans_serializer , "invetoryTrans" :inventory_serialize_and_Entry , "inventory_entry_avail" : inventory_entry_available }
    else:
        return {"status" : False}


def purchaseVoucher(voucherId, data):
    data = dict(data)
    voucherTransData = {
        # "voucherTransactionId" : str(uuid4()),
        "voucher" : voucherId,
        "product" : data['product'],
        "warehouse" : data['warehouse'],
        "rate": data["rate"],
        "quantity":  data["quantity"],
        "amount":  data["amount"],
        "vatPercentage":  data["vatPercentage"],
        "vatAmount":  data["vatAmount"],
        "TotalAmount":  data["TotalAmount"]
    }

    warehouseTrans_data = {
        "voucher" : voucherId,
        "warehouse" : data['warehouse'],
        "product" : data['product'],
        "quantity" : Decimal(data["quantity"]),
    }

    voucherTrans_serialize = VoucherTransactionWriteSerializerApp(data=voucherTransData)

    
    warehouseTrans_serializer = WarehouseTransactionWriteSerializerApp(data=warehouseTrans_data)

    # Inventory
    inventory_entry_available = True
    inventory_serialize_and_Entry = None
    try:
        inventory_serialize_and_Entry = Inventory.objects.get(product = data['product'] , warehouse = data['warehouse'])
        inventory_serialize_and_Entry.quantity += Decimal(data["quantity"])

    except Inventory.DoesNotExist:
        inventory_entry_available = False
        inventory_data = {
        "product" : data['product'],
        "warehouse" : data['warehouse'],
        "rate" : data["rate"],
        "quantity" : Decimal(data["quantity"]),
        }
        inventory_serialize_and_Entry = InventoryWriteSerializerApp(data = inventory_data)
    
    if voucherTrans_serialize.is_valid() and warehouseTrans_serializer.is_valid() :
        if inventory_entry_available == False and inventory_serialize_and_Entry.is_valid() == False:
            return {"status" : False} 
        return {"status" : True , "voucherTrans" : voucherTrans_serialize , "warehouseTrans" : warehouseTrans_serializer , "invetoryTrans" :inventory_serialize_and_Entry , "inventory_entry_avail" : inventory_entry_available }
    else:
        return {"status" : False}
        
    

def mainVoucherActions(vouchertype , voucherId , data):
    try:
        if str(vouchertype).strip().lower() == 'sales':
            return salesVoucher(voucherId, data)
        elif str(vouchertype).strip().lower() == 'purchase':
            return purchaseVoucher(voucherId, data)
    except Exception as error:
        return {"status" : False}
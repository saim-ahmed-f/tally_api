from django.db import models
import uuid
from django.utils import timezone

from product.models import Product
from warehouse.models import Warehouse
from voucher.models import Voucher

# Create your models here.

class VoucherTransaction(models.Model):
    voucherTransactionId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    voucher = models.ForeignKey(
    Voucher,
    on_delete=models.CASCADE,
    related_name='allInventory',

    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='voucherTransaction_product'
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='voucherTransaction_warehouse'
    )


    rate = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )

    quantity  = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )


    amount  = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )
    

    vatPercentage  = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )


    vatAmount  = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )

    TotalAmount  = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )


    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return f"{self.voucher} - {self.created_on}"
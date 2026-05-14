from django.db import models
import uuid
from django.utils.timezone import now


from product.models import Product
from warehouse.models import Warehouse
from voucher.models import Voucher

class warehouseTransaction(models.Model):

    warehouseTransactionId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    voucher = models.ForeignKey(
    Voucher,
    on_delete=models.CASCADE,
    related_name='warehouseTransaction_voucher',
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='warehouseTransaction_product'
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='warehouseTransaction_warehouse'
    )

    quantity  = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )

    onTally = models.BooleanField(default=True)


    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)


    def __str__(self):
        return f"{self.product} - {self.warehouse} - {str(self.quantity)}"

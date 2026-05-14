from django.db import models
import uuid
from django.utils import timezone


from product.models import Product
from warehouse.models import Warehouse

class Inventory(models.Model):

    inventoryId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    #  GUID = models.CharField(max_length=100 , unique=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory_product'
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='inventory_warehouse'
    )


    rate = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )

    quantity  = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
    )

    onTally = models.BooleanField(default=True)


    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.product} - {self.warehouse} - {str(self.rate)} - {str(self.quantity)}"

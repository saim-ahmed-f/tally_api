from django.db import models
import uuid
from django.utils import timezone
# Create your models here.


class Warehouse(models.Model):

    warehouseId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    warehouseGUID = models.CharField(max_length=100 , unique=True , null=True)

    warehouseName = models.CharField(max_length=100)

    onTally = models.BooleanField(default=True)


    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.warehouseName

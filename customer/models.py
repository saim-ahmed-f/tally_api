from django.db import models
import uuid
from django.utils.timezone import now
# Create your models here.
from salesman.models import Salesman


class Customer(models.Model):

    customerId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    customerGUID = models.CharField(max_length=100 , unique=True, null=True)

    customerCode = models.CharField(max_length=100 , unique=True)

    customerName = models.CharField(max_length=100)

    salesman = models.ForeignKey(
        Salesman,
        on_delete=models.CASCADE,
        related_name='customers'
    )

    onTally = models.BooleanField(default=True)

    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)
    


    def __str__(self):
        return f"{self.customerName}"
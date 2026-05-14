from django.db import models
import uuid
from django.utils import timezone
# Create your models here.

from salesman.models import Salesman
from customer.models import Customer
from voucher_type.models import VoucherType


class Voucher(models.Model):

    voucherId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    voucherGUID = models.CharField(max_length=100 , unique=True , null=True)
    

    voucherDate = models.DateField(default=timezone.now)

    voucherNumber = models.CharField(max_length=50 , unique=True)

    voucherRemark = models.TextField(default="Remark....")

    # ? Relations with other Tables

    salesman = models.ForeignKey(
        Salesman,
        on_delete=models.CASCADE,
        related_name='voucherSalesman'
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='voucherCustomer'
    )

    voucherType = models.ForeignKey(
        VoucherType,
        on_delete=models.CASCADE,
        related_name='voucherType'
    )

    onTally = models.BooleanField(default=True)

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created (not updated)
            self.updated_on = self.created_on
        else:
            self.updated_on = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.voucherNumber} - {self.created_on}"
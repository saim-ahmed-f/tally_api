from django.db import models
from django.utils import timezone
import uuid
# Create your models here.
from voucher.models import Voucher


class Receipt(models.Model):

    receiptId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    recceiptGUID = models.CharField(max_length=100 , unique=True , null=True)


    PAYMENT_MODE_CHOICES = [
        ('cash', 'cash'),
        ('bank', 'bank'),
    ]

    class paymentStatusSelection(models.TextChoices):
        PENDING = 'pending','pending'
        PAID = "paid" , "paid"
        CANCEL = "cancel", "cancel"

    paymentMode = models.CharField(
        max_length=10,
        choices=PAYMENT_MODE_CHOICES,
        default="cash",
    )

    paymentStatus = models.CharField(
        max_length=20,
        choices=paymentStatusSelection.choices,
        default= paymentStatusSelection.PAID
    )

    voucher = models.ForeignKey(
    Voucher,
    on_delete=models.CASCADE,
    related_name='receipt_voucher',
    )

    paymentDate = models.DateField(default=timezone.now)

    paymentAmount  = models.DecimalField(
        max_digits=10,  # total digits (including decimals)
        decimal_places=2  # digits after decimal point
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
        return f"{self.receiptId} - {self.voucher.voucherNumber}"


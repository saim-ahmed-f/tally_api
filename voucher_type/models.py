from django.db import models
import uuid
from django.utils import timezone
# Create your models here.


class VoucherType(models.Model):
    
    voucherName = models.CharField(max_length=100 , primary_key=True,editable=True)

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.voucherName}"


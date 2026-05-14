from django.db import models
import uuid
from django.utils import timezone
# Create your models here.

class Product(models.Model):


    class baseUnitSelection(models.TextChoices):
        KG = 'kg', 'kg'
        NOS = 'nos', 'nos'
        PCS = 'pcs', 'pcs'


    productId  = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    productGUID = models.CharField(max_length=100 , unique=True, null=True)

    productCode = models.CharField(max_length=100 , unique=True)

    productName = models.CharField(max_length=100)
    
    baseUnit = models.CharField(
        max_length=20,
        choices=baseUnitSelection.choices,
        default=baseUnitSelection.NOS,
    )

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)


    onTally = models.BooleanField(default=True)
    
    

    def __str__(self):
        return f"{self.productName}"


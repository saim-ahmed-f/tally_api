from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
# Create your models here.


class Salesman(AbstractUser):
    salesmanId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True
    )

    salesmanGUID = models.CharField(max_length=100 , unique=True , null=True)

    salesmanName = models.CharField(max_length=100)

    salesmanCode = models.CharField(max_length=100 , unique=True)


    salesmanPhoneNumber = models.CharField(max_length=15)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('salesman', 'Salesman'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='salesman')


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
        return f"{self.salesmanName}"



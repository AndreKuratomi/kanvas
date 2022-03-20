from django.db import models
import uuid


class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    zip_code = models.CharField(max_length=255, unique=False)

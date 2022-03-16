from django.db import models


class Address(models.Model):
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    zip_code = models.CharField(max_length=255, unique=False)

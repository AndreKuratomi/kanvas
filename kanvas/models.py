from types import CoroutineType
from django.db import models
import uuid


class Course(models.Model):
    uuid: models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name: models.CharField(max_length=255, unique=True)
    demo_time: models.TimeField()
    created_at: models.DateTimeField()
    link_repo: models.CharField(max_length=255)


class Address(models.Model):
    uuid: models.UUIDField(default=uuid.uuid4, editable=False)
    city: models.CharField(max_length=255)
    country: models.CharField(max_length=255)
    state: models.CharField(max_length=255)
    street: models.CharField(max_length=255)
    house_number: models.IntegerField()
    zip_code: models.CharField(max_length=255, unique=False)

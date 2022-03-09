from tkinter import CASCADE
from django.db import models
import uuid


class User(models.Model):
    uuid: models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    is_admin: models.BooleanField()
    email: models.CharField(max_length=255, unique=True)
    password: models.CharField(max_length=255)
    first_name: models.CharField(max_length=255)
    last_name: models.CharField(max_length=255)

    address: models.ForeignKey("Address", on_delete=models.CASCADE, related_name="users")


class Course(models.Model):
    uuid: models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name: models.CharField(max_length=255, unique=True)
    demo_time: models.TimeField()
    created_at: models.DateTimeField()
    link_repo: models.CharField(max_length=255)

    # if user.is_admin == True:
    user_instructor = models.OneToOneField(User, default=str, on_delete=models.CASCADE)
    # if user.is_admin == False:
    user_students = models.ManyToManyField(User, related_name="students")


class Address(models.Model):
    uuid: models.UUIDField(default=uuid.uuid4, editable=False)
    city: models.CharField(max_length=255)
    country: models.CharField(max_length=255)
    state: models.CharField(max_length=255)
    street: models.CharField(max_length=255)
    house_number: models.IntegerField()
    zip_code: models.CharField(max_length=255, unique=False)

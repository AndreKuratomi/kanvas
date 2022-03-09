from django.db import models


class User(models.Model):
    is_admin = models.BooleanField()
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    address = models.ForeignKey("Address", on_delete=models.CASCADE, related_name="users")


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    demo_time = models.TimeField()
    link_repo = models.CharField(max_length=255)

    # if user.is_admin == True:
    user_instructor = models.OneToOneField(User, default=str, on_delete=models.CASCADE)
    # if user.is_admin == False:
    user_students = models.ManyToManyField(User, related_name="students")


class Address(models.Model):
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    zip_code = models.CharField(max_length=255, unique=False)

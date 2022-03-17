from django.db import models
from accounts.models import PersonalizedUser
import uuid


class Courses(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    name = models.CharField(max_length=255, unique=True)
    demo_time = models.TimeField()
    link_repo = models.CharField(max_length=255)

    instructor = models.OneToOneField(PersonalizedUser, null=True, on_delete=models.CASCADE, related_name="course")
    students = models.ManyToManyField(PersonalizedUser, related_name="courses")

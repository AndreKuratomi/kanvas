from django.db import models
from users.models import PersonalizedUser


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    demo_time = models.TimeField()
    link_repo = models.CharField(max_length=255)

    user_instructor = models.OneToOneField(PersonalizedUser, on_delete=models.CASCADE)
    user_students = models.ManyToManyField(PersonalizedUser, related_name="students")

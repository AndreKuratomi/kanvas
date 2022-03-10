from django.db import models
from users.models import PersonalizedUser


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    demo_time = models.TimeField()
    link_repo = models.CharField(max_length=255)

    # if user.is_admin == True:
    user_instructor = models.OneToOneField(PersonalizedUser, default=str, on_delete=models.CASCADE)
    # if user.is_admin == False:
    user_students = models.ManyToManyField(PersonalizedUser, related_name="students")

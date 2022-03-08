from django.db import models


class Course(models.Model):
    uuid: models.UUIDField(read_only=True, unique=True)
    name: models.CharField(max_length=255, unique=True)
    demo_time: models.TimeField()
    created_at: models.DateTimeField(read_only=True)
    link_repo: models.CharField(max_length=255)

# Create your models here.

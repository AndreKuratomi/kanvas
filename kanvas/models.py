from django.db import models
import uuid


class Course(models.Model):
    uuid: models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    name: models.CharField(max_length=255, unique=True)
    demo_time: models.TimeField()
    created_at: models.DateTimeField()
    link_repo: models.CharField(max_length=255)

# Create your models here.

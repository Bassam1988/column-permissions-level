
# message type code be Error or Notification
from django.db import models
import uuid

from classes.GeneralFunctions import default_value

from .models import Status


class ErrorType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    code_name = models.CharField(max_length=6)
    description = models.CharField(max_length=300)
    status = models.ForeignKey(
        Status, on_delete=models.SET(default_value(Status)))
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.name


class Error(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(
        ErrorType, on_delete=models.SET(default_value(ErrorType)))
    name = models.CharField(max_length=30)
    code_name = models.CharField(max_length=6)
    description = models.CharField(max_length=300)
    message_text = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(
        Status, on_delete=models.SET(default_value(Status)))

    @property
    def get_name(self):
        return self.name
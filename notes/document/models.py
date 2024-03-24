from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings

from django.db import models


class NotesUser(AbstractUser):
    id = models.AutoField(primary_key=True)


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    is_private = models.BooleanField(default=False)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

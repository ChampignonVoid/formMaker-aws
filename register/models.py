import uuid
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    email_confirmed = models.BooleanField(default=False)


class EmailValidationToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

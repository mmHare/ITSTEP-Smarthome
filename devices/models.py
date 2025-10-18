from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    device_name = models.CharField("name", max_length=200)
    device_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.device_name

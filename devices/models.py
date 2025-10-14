from django.db import models


class Device(models.Model):
    device_name = models.CharField("name", max_length=200)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.device_name

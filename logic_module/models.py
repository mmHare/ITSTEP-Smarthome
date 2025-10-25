from django.db import models

from devices.models import Device


class LogicController(models.Model):
    LOGIC_CHOICES = [
        ('thermal', 'Thermal Logic'),
        ('time', 'Time Logic'),
    ]

    logic_type = models.CharField(max_length=20, choices=LOGIC_CHOICES)
    mac_address = models.CharField(max_length=11)
    active = models.BooleanField(default=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    numeric_max = models.FloatField()
    numeric_min = models.FloatField()
    time_max = models.TimeField()
    time_min = models.TimeField()

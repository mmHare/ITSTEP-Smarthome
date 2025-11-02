from django.db import models

from devices.models import Device


class LogicController(models.Model):
    LOGIC_CHOICES = [
        ('thermal', 'Thermal Logic'),
        ('time', 'Time Logic'),
    ]

    name = models.CharField("name", max_length=200, default="Rule")
    logic_type = models.CharField(max_length=20, choices=LOGIC_CHOICES)
    mac_address = models.CharField(max_length=11)
    active = models.BooleanField(default=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    numeric_max = models.FloatField(blank=True, null=True)
    numeric_min = models.FloatField(blank=True, null=True)
    time_max = models.TimeField(blank=True, null=True)
    time_min = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name

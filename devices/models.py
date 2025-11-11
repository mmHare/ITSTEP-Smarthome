from django.db import models
from django.contrib.auth.models import User


class DeviceRoom(models.Model):
    room_name = models.CharField("name", max_length=200)

    def __str__(self):
        return self.room_name


class DeviceType(models.Model):
    type_name = models.CharField("name", max_length=200)
    is_active = models.BooleanField("active", default=True)

    enable_thermal = models.BooleanField("Enable thermal rules", default=False)
    enable_time = models.BooleanField("Enable time rules", default=False)

    def __str__(self):
        return self.type_name

    def get_rule_types(self) -> list:
        """Returns str list of enabled logic types"""
        result = []
        if self.enable_thermal:
            result.append("thermal")
        if self.enable_time:
            result.append("time")
        return result


class Device(models.Model):
    device_name = models.CharField("name", max_length=200)
    device_user = models.ForeignKey(
        User, verbose_name="user", on_delete=models.CASCADE)
    device_type = models.ForeignKey(
        DeviceType, verbose_name="type", on_delete=models.CASCADE)
    device_room = models.ForeignKey(
        DeviceRoom, verbose_name="room", default=None, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.BooleanField("on", default=False)

    def __str__(self):
        return self.device_name

    def set_state(self, value: bool):
        self.state = value

    def get_state(self):
        return self.state

    def turn_on(self):
        self.set_state(True)

    def turn_off(self):
        self.set_state(False)

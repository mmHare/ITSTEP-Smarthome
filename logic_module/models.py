from django.db import models

from devices.models import Device
from logic_module.logic.logic_map import LOGIC_MAP


class LogicController(models.Model):
    # used for DeviceDetailView
    LOGIC_CHOICES = [
        ('thermal', 'Thermal Logic'),
        ('time', 'Time Logic'),
    ]

    name = models.CharField("name", max_length=200, default="Rule")
    mac_address = models.CharField(max_length=11)
    active = models.BooleanField(default=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    numeric_value = models.FloatField(blank=True, null=True)
    numeric_max = models.FloatField(blank=True, null=True)
    numeric_min = models.FloatField(blank=True, null=True)
    time_max = models.TimeField(blank=True, null=True)
    time_min = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def update_value(self, num_value):
        self.numeric_value = num_value  # set current value from device

    def get_state(self) -> bool:
        """Checks if conditions for rules are met"""
        # if controller is off, conditions are not checked
        if not self.active:
            return
        try:
            result = self.device.state
            if not self.numeric_value:
                raise Exception("Controller has no current value")

            for logic in self.device.device_type.get_rule_types():
                LogicClass = LOGIC_MAP.get(logic)
                if not LogicClass:
                    continue
                logic_instance = LogicClass(self)
                result = result or logic_instance.check()

            return result
        except Exception as e:
            print("Error while updating device state:", e)

import datetime
from django.db import models

from devices.models import Device
from logic_module.logic.logic_map import LOGIC_MAP


class LogicController(models.Model):
    # used for DeviceDetailView; deprecated
    # LOGIC_CHOICES = [
    #     ('thermal', 'Thermal Logic'),
    #     ('time', 'Time Logic'),
    # ]

    item_kind = "logic rule"

    name = models.CharField("name", max_length=200, default="Rule")
    mac_address = models.CharField(max_length=11)
    active = models.BooleanField(default=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    numeric_value = models.FloatField(blank=True, null=True)
    numeric_max = models.FloatField(default=0)
    numeric_min = models.FloatField(default=0)
    time_min = models.TimeField(default=datetime.time(8, 00))
    time_max = models.TimeField(default=datetime.time(22, 00))

    def __str__(self):
        return self.name

    def update_value(self, num_value):
        try:
            # set current value from device
            self.numeric_value = float(num_value)
            self.save()
        except:
            raise

    def get_state(self) -> bool:
        """Checks if conditions for rules are met"""
        # if controller is off, conditions are not checked
        if not self.active:
            return
        try:
            result = self.device.state
            if self.device.device_type.get_show_numeric_fields() and not self.numeric_value:
                raise Exception("Controller has no current value")

            result = True
            for logic in self.device.device_type.get_rule_types():
                LogicClass = LOGIC_MAP.get(logic)
                if not LogicClass:
                    continue
                logic_instance = LogicClass(self)
                result = logic_instance.check() and result

            return result
        except Exception as e:
            print("Error while updating device state:", e)

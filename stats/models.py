from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class StatsUserAction(models.Model):
    user = models.ForeignKey(User, verbose_name="user",
                             on_delete=models.CASCADE)
    timestamp = models.DateTimeField("timestamp", default=timezone.now)
    user_action = models.CharField("user_action", max_length=200)

    # on which item (device, rule, etc.) action was performed
    item_id = models.IntegerField("item_id", null=True, blank=True)
    item_name = models.CharField(
        "item_name", max_length=200, null=True, blank=True)
    item_kind = models.CharField(
        "item_kind", max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.action}'
    
    @property
    def user_name(self):
        return self.user.username

    @property
    def time_as_str(self) -> str:
        return self.timestamp.strftime("%Y/%m/%d %H:%M:%S")


class StatsDeviceState(models.Model):
    # we don't do foreign key, so we don't loose record after device is deleted
    device_id = models.IntegerField("device_id")
    device_name = models.CharField("device_name", max_length=200)
    device_kind = models.CharField("device_kind", max_length=200)
    timestamp = models.DateTimeField("timestamp", default=timezone.now)

    device_on = models.BooleanField("device_on")
    metric = models.CharField("metric", max_length=200, null=True, blank=True)
    value = models.FloatField("value", null=True, blank=True)
    description = models.CharField(
        "description", max_length=200, null=True, blank=True)

    @property
    def time_as_str(self) -> str:
        return self.timestamp.strftime("%Y/%m/%d %H:%M:%S")

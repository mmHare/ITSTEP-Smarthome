from django.utils import timezone
from django.contrib.auth.models import User

from devices.models import Device
from stats.models import StatsDeviceState, StatsUserAction


class StatsService:
    @classmethod
    def save_user_action(cls, user: User, action: str, item: dict = None):
        """Saves history record of user action

        Args:
            user (User): user that performed action
            action (str): e.g. 'add', 'delete', 'edit'
            item (dict, optional): details of item that action was performed on (item_id, item_name)
        """
        try:
            new_record = StatsUserAction(
                user=user,
                timestamp=timezone.now(),
                user_action=action
            )
            if item:
                new_record.item_id = item.get("item_id")
                new_record.item_name = item.get("item_name")
                new_record.item_kind = item.get("item_kind")

            new_record.save()
        except Exception as e:
            print("Error while adding user action record:", e)

    @classmethod
    def save_device_state(cls, device: Device, metric: str = None, value: float = None):
        """Saves history record of device state, metric and value"""
        try:
            if not isinstance(device, Device):
                raise TypeError('"device" parameter must be of Device class')

            new_record = StatsDeviceState(
                device_id=device.id,
                device_name=device.device_name,
                device_kind=device.item_kind,
                timestamp=timezone.now(),
                device_on=device.state,
                metric=metric,  # to be implemented from sensor
                value=value  # to be implemented from sensor
            )

            new_record.save()

        except Exception as e:
            print("Error while adding device state record:", e)

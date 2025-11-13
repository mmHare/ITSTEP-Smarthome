from datetime import datetime
from django.utils import timezone

from stats.models import StatsDeviceState, StatsUserAction


class StatsService:
    @classmethod
    def save_user_action(cls, user, action: str, item: dict = None):
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
    def save_device_state(cls, device, metric: str = None, value: float = None):
        """Saves history record of device state, metric and value

        Args:
            device (Device): Device object model of interest 
            metric (str, optional): unit name, yet to be implemented
            value (float, optional): yet to be implemented
        """
        from devices.models import Device
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

    @classmethod
    def export_user_action_history(cls, user, format: str = 'json', time_from: datetime = None, time_to: datetime = None):
        """Export historic user action data into json or csv

        Args:
            user (User): selected user (None for all users)
            format (str, optional): json or csv. Defaults to 'json'.
            time_from (datetime, optional): Start time (None for all previous data). Defaults to None.
            time_to (datetime, optional): End time (None for current time). Defaults to None.
        """
        if not user:
            pass  # export for all users

    @classmethod
    def export_device_history(cls, device, format: str = 'json', time_from: datetime = None, time_to: datetime = None):
        """Export historic device data into json or csv

        Args:
            device (Device): selected device (None for all devices)
            format (str, optional): json or csv. Defaults to 'json'.
            time_from (datetime, optional): Start time (None for all previous data). Defaults to None.
            time_to (datetime, optional): End time (None for current time). Defaults to None.
        """

        if not device:
            pass

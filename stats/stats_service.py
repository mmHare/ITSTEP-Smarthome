from datetime import datetime
from django.utils import timezone

from stats.models import StatsDeviceState, StatsUserAction


class StatsService:
    @classmethod
    def save_user_action(cls, user, action: str, item=None):
        """Saves history record of user action

        Args:
            user (User): user that performed action
            action (str): e.g. 'add', 'delete', 'edit'
            item (dict, optional): details of item that action was performed on (item_id, item_name)
        """

        def action_str(action: str) -> str:
            return action.strip().capitalize().replace('_', ' ')

        try:
            new_record = StatsUserAction(
                user=user,
                timestamp=timezone.now(),
                user_action=action_str(action)
            )
            if item:
                if isinstance(item, dict):
                    # check dictionary keys
                    new_record.item_id = item.get("item_id")
                    new_record.item_name = item.get("item_name")
                    new_record.item_kind = item.get("item_kind")
                else:
                    # check object properties (models need to have it)
                    new_record.item_id = getattr(item, "id", None)
                    new_record.item_name = getattr(item, "name", None)
                    new_record.item_kind = getattr(item, "item_kind", None)

            new_record.save()
        except Exception as e:
            print("Error while adding user action record:", e)

    @classmethod
    def save_device_state(cls, device, metric: str = None, value: float = None, description: str = None):
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
                value=value,  # to be implemented from sensor
                description=description
            )

            new_record.save()

        except Exception as e:
            print("Error while adding device state record:", e)

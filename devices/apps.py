import time
from django.apps import AppConfig


class DevicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devices'

    def ready(self):
        from logic_module.models import LogicController

        def check_devices():
            while True:
                for device_control in LogicController.objects.all():
                    if device_control.active:
                        device_control.update_device_state()
                time.sleep(30)

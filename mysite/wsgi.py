"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import threading
import time

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()


def start_device_check_thread():
    from logic_module.models import LogicController
    from devices.models import Device
    from django.db import OperationalError, connections

    def check_devices():
        db_conn = connections['default']
        while True:
            try:
                db_conn.ensure_connection()
                break
            except OperationalError:
                # Waiting for database to become available...
                time.sleep(5)

        while True:
            try:
                for dvc in Device.objects.filter(power_on=True):
                    dvc.monitor_device()  # save state history record
                    # check all active conditions for device
                    states = [ctrl.get_state() for ctrl in LogicController.objects.filter(
                        active=True, device=dvc)]
                    # skip get_state() returned None
                    valid_states = [s for s in states if s is not None]

                    if valid_states:
                        # device state will be True if any condition is met
                        new_state = any(valid_states)
                        if new_state != dvc.state:
                            # dvc.state = new_state
                            dvc.set_state(new_state)
                            dvc.save()
            except OperationalError as e:
                print(f"Database not ready: {e}")
            except Exception as e:
                print(f"Error in device check thread: {e}")
            time.sleep(5)

    thread = threading.Thread(target=check_devices, daemon=True)
    thread.start()


# Uncomment to start background thread
start_device_check_thread()

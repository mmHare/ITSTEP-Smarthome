from django.contrib import admin

from devices.models import DeviceRoom, DeviceType, Device

admin.site.register(DeviceRoom)
admin.site.register(DeviceType)
admin.site.register(Device)

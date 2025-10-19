from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('device_name', 'device_type', 'device_room')

    # def is_valid(self):
    #     return True

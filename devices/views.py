from django.shortcuts import redirect, render
from django.views import generic

from .models import Device


def devices_home_view(request):
    user_name = request.user.username

    if not user_name:
        return redirect('smarthome:login')

    user_devices = Device.objects.filter(device_user=request.user)

    return render(request, 'devices/home.html', {
        'user_name': user_name,
        'devices': user_devices
    })


class DetailView(generic.DetailView):
    model = Device
    template_name = "devices/details.html"
    context_object_name = "device"

    def get_queryset(self):
        # Only return devices belonging to the logged-in user
        return Device.objects.filter(device_user=self.request.user)

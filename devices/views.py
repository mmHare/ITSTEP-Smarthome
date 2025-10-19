from django.shortcuts import redirect, render
from django.views import generic

from devices.forms import DeviceForm

from .models import Device


from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


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


def new_device_view(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)  # don't save yet
            device.device_user = request.user
            device.save()

            return redirect('devices:home')
        print('not valid')
    else:
        form = DeviceForm()
    return render(request, 'devices/new_device.html', {'form': form})


class DeviceUpdateView(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'devices/device_form.html'
    success_url = reverse_lazy('devices:home')

    def get_queryset(self):
        # Restrict editing to the logged-in user's devices
        return Device.objects.filter(device_user=self.request.user)


def delete_device_view(request, pk):
    device = get_object_or_404(
        Device, pk=pk, device_user=request.user)  # ensures ownership

    if request.method == 'POST':
        device.delete()
        return redirect('devices:home')

    # Optional: confirmation page (could skip and delete immediately)
    return render(request, 'devices/confirm_delete.html', {'device': device})

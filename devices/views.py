from django.shortcuts import redirect, render
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .forms import DeviceForm
from .models import Device, DeviceRoom


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
    return render(request, 'devices/device_form.html', {'form': form})


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


def room_list_view(request):
    error_text = ''
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            if name:
                if DeviceRoom.objects.filter(room_name=name).exists():
                    error_text = 'This room is already in the list'
                else:
                    DeviceRoom.objects.create(room_name=name)

        except DeviceRoom.DoesNotExist:
            error_text = 'Room does not exist'
            # return render(request, 'devices/room_list.html', {'error': 'Room does not exist'})

    device_rooms = DeviceRoom.objects.filter()

    return render(request, 'devices/room_list.html', {
        'rooms': device_rooms,
        'error': error_text,
    })


def delete_device_view(request, pk):
    room = get_object_or_404(DeviceRoom, pk=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('devices:room_list')

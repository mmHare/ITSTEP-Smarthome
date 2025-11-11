import json
from typing import Any
from django.shortcuts import redirect, render
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from logic_module.forms import LogicControllerForm
from logic_module.models import LogicController
from stats.stats_service import StatsService

from .forms import DeviceForm
from .models import Device, DeviceRoom

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST


def devices_home_view(request):
    user_name = request.user.username

    if not user_name:
        return redirect('smarthome:login')

    user_devices = Device.objects.filter(device_user=request.user)

    return render(request, 'devices/home.html', {
        'user_name': user_name,
        'devices': user_devices
    })


@method_decorator(ensure_csrf_cookie, name='dispatch')
class DeviceDetailView(generic.DetailView):
    model = Device
    template_name = "devices/details.html"
    context_object_name = "device"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        device = self.get_object()

        # Fields are shown depending on what is enabled in current device's device type
        show_numeric = device.device_type.get_show_numeric_fields()
        show_time = device.device_type.get_show_time_fields()

        context["logic_form"] = LogicControllerForm(
            show_numeric=show_numeric, show_time=show_time)
        # context["logic_types"] = LogicController.LOGIC_CHOICES
        context["logic_controllers"] = LogicController.objects.filter(
            device=device)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Fields are shown depending on what is enabled in current device's device type
        show_numeric = self.object.device_type.get_show_numeric_fields()
        show_time = self.object.device_type.get_show_time_fields()

        form = LogicControllerForm(
            request.POST or None,
            show_numeric=show_numeric,
            show_time=show_time
        )

        if form.is_valid():
            logic = form.save(commit=False)
            logic.device = self.object
            # logic.logic_type = selected_type
            logic.save()

            # success, so save history record
            record_item = {"item_id": logic.id,
                           "item_name": logic.name,
                           "item_kind": logic.item_kind}
            StatsService.save_user_action(request.user, 'add', record_item)

            return redirect("devices:details", pk=self.object.pk)

        # context = self.get_context_data()
        context = self.get_context_data(object=self.object)
        context["logic_form"] = form
        return self.render_to_response(context)

    def edit_value(request):
        form = LogicControllerEditForm()
        return render(request, 'devices/details.html', {'form': form})


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

    device_rooms = DeviceRoom.objects.filter()

    return render(request, 'devices/room_list.html', {
        'rooms': device_rooms,
        'error': error_text,
    })


def delete_room_view(request, pk):
    room = get_object_or_404(DeviceRoom, pk=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('devices:room_list')


@require_POST
def toggle_logic_active(request, pk):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    is_active = data.get('active')
    if not isinstance(is_active, bool):
        return JsonResponse({'success': False, 'error': 'Invalid active value'}, status=400)

    try:
        rule = LogicController.objects.get(pk=pk)
    except LogicController.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)

    rule.active = is_active
    rule.save()
    return JsonResponse({'success': True, 'active': rule.active})


def rule_action(request, pk):
    """Performs back-end action on rule according to sent json data"""
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    action = data.get('action')
    if not isinstance(action, str):
        return JsonResponse({'success': False, 'error': 'Invalid action value'}, status=400)

    try:
        rule = LogicController.objects.get(pk=pk)
    except LogicController.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)

    # get item data for action history
    record_item = {"item_id": rule.id,
                   "item_name": rule.name,
                   "item_kind": rule.item_kind}

    # execute actions
    if action == 'delete':
        rule.delete()
    elif action == 'edit':
        param_dict = data.get('param_dict')
        rule.update_value(param_dict)
    else:
        return JsonResponse({'success': False, 'error': 'Action not recognized'}, status=400)

    # success, so save history record
    StatsService.save_user_action(request.user, action, record_item)

    return JsonResponse({'success': True, 'action': action})

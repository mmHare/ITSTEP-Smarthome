import json
from typing import Any
from django.shortcuts import redirect, render
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from logic_module.forms import LogicControllerForm
from logic_module.models import LogicController
from stats.stats_service import StatsService

from .forms import DeviceForm
from .models import Device, DeviceRoom

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.db.models import Max


def devices_home_view(request):
    user = request.user

    if not user.username:
        return redirect('smarthome:login')

    if user.is_staff:
        user_devices = Device.objects.filter()
    else:
        user_devices = Device.objects.filter(device_user=request.user)

    return render(request, 'devices/home.html', {
        'user_name': user.username,
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
            logic.save()

            # success, so save history record
            action = 'add'
            StatsService.save_user_action(request.user, action, logic)

            return redirect("devices:details", pk=self.object.pk)

        context = self.get_context_data(object=self.object)
        context["logic_form"] = form
        return self.render_to_response(context)


def new_device_view(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)  # don't save yet
            device.device_user = request.user  # set user before saving
            device.save()

            # save to action history
            action = 'add'
            StatsService.save_user_action(request.user, action, device)

            return redirect('devices:home')
        print('not valid')
    else:
        form = DeviceForm()
    return render(request, 'devices/device_form.html', {'form': form})


def new_rule_view(request, pk):
    device = get_object_or_404(
        Device, pk=pk
    )

    if request.method == 'POST':
        # Fields are shown depending on what is enabled in current device's device type
        show_numeric = device.device_type.get_show_numeric_fields()
        show_time = device.device_type.get_show_time_fields()

        form = LogicControllerForm(
            request.POST, show_numeric=show_numeric, show_time=show_time)
        if form.is_valid():
            rule = form.save(commit=False)  # don't save yet
            rule.rule_user = request.user  # set user before saving
            rule.save()

            # save to action history
            action = 'add'
            StatsService.save_user_action(request.user, action, rule)

            return redirect('devices:details')
        print('not valid')
    else:
        form = LogicControllerForm()
    return render(request, 'devices/rule_form.html', {'form': form})


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
        # save to action history
        action = 'delete'
        StatsService.save_user_action(request.user, action, device)

        device.delete()
        return redirect('devices:home')


class RuleUpdateView(UpdateView):
    model = LogicController
    form_class = LogicControllerForm
    template_name = 'devices/rule_form.html'
    success_url = reverse_lazy('devices:details')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        rule = self.get_object()
        device = rule.device

        # Fields are shown depending on what is enabled in current device's device type
        show_numeric = device.device_type.get_show_numeric_fields()
        show_time = device.device_type.get_show_time_fields()

        context["logic_form"] = LogicControllerForm(
            show_numeric=show_numeric, show_time=show_time)
        context["device"] = LogicController.objects.filter(
            device=device)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Fields are shown depending on what is enabled in current device's device type
        show_numeric = self.object.device.device_type.get_show_numeric_fields()
        show_time = self.object.device.device_type.get_show_time_fields()

        form = LogicControllerForm(
            request.POST or None,
            show_numeric=show_numeric,
            show_time=show_time
        )

        if form.is_valid():
            logic = form.save(commit=False)
            logic.device = self.object
            logic.save()

            # success, so save history record
            action = 'add'
            StatsService.save_user_action(request.user, action, logic)

            return redirect("devices:details", pk=self.object.device.pk)

        context = self.get_context_data(object=self.object)
        context["logic_form"] = form
        return self.render_to_response(context)

    def get_queryset(self):
        # Restrict editing to the logged-in user's devices
        return LogicController.objects.filter()


def room_list_view(request):
    error_text = ''
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            if name:
                if DeviceRoom.objects.filter(room_name=name).exists():
                    error_text = 'This room is already in the list'
                else:
                    room = DeviceRoom.objects.create(room_name=name)

                    # save to action history
                    action = 'add'
                    StatsService.save_user_action(request.user, action, room)

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
        # save to action history
        action = 'delete'
        StatsService.save_user_action(request.user, action, room)

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

    # save to action history
    action = 'turn_on' if is_active else 'turn_off'
    StatsService.save_user_action(request.user, action, rule)

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

    # get item data for action history, here in case of deletion
    record_item = {"item_id": rule.id,
                   "item_name": rule.name,
                   "item_kind": rule.item_kind}

    parent_device = rule.device  # for redirect

    # execute actions
    if action == 'delete':
        rule.delete()
    elif action == 'set_value':
        param_dict = data.get('param_dict')
        rule.update_value(param_dict['input_value_num'])
    else:
        return JsonResponse({'success': False, 'error': 'Action not recognized'}, status=400)

    # success, so save history record
    StatsService.save_user_action(request.user, action, record_item)

    return JsonResponse({'success': True, 'action': action, 'details_url': reverse('devices:details', args=[parent_device.id])})


def toggle_power(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        if device.power_on:  # if device is turned on, we power it off
            device.turn_off()
            device.save()
            StatsService.save_user_action(request.user, "power_off", device)
        else:
            device.turn_on()
            device.save()
            StatsService.save_user_action(request.user, "power_on", device)

        return redirect('devices:home')


def check_status(request):
    last_update = Device.objects.aggregate(Max("updated"))["updated__max"]
    latest_seen = request.session.get("last_seen_update")

    # First time → store and return no refresh
    if latest_seen is None:
        request.session["last_seen_update"] = str(last_update)
        return JsonResponse({"refresh_required": False})

    refresh_needed = str(last_update) > latest_seen

    if refresh_needed:
        request.session["last_seen_update"] = str(last_update)

    return JsonResponse({"refresh_required": refresh_needed})

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

from .forms import DeviceForm
from .models import Device, DeviceRoom, DeviceType

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
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
        context["logic_form"] = LogicControllerForm()
        # (show_numeric=False, show_time=False)
        context["logic_types"] = LogicController.LOGIC_CHOICES
        context["logic_controllers"] = LogicController.objects.filter(
            device=device)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        selected_type = request.POST.get("logic_option")

        # Decide which fields to show based on logic type
        show_numeric = selected_type == 'thermal'
        show_time = selected_type == 'time'

        form = LogicControllerForm(
            request.POST or None,
            show_numeric=show_numeric,
            show_time=show_time
        )

        if form.is_valid():
            logic = form.save(commit=False)
            logic.device = self.object
            logic.logic_type = selected_type
            logic.save()
            return redirect("devices:details", pk=self.object.pk)

        # context = self.get_context_data()
        context = self.get_context_data(object=self.object)
        context["logic_form"] = form
        return self.render_to_response(context)


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


# @csrf_exempt  # (optional for simplicity, see note below)
# @ensure_csrf_cookie
# @require_POST
# def toggle_logic_active(request, pk):
#     try:
#         logic = LogicController.objects.get(pk=pk)
#         active = request.POST.get('active') == 'true'
#         logic.active = active
#         logic.save()
#         return JsonResponse({'success': True, 'active': logic.active})
#     except LogicController.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Logic not found'}, status=404)
# # @ensure_csrf_cookie
# # @require_POST
# # def toggle_logic_active(request, rule_id):
# #     if request.method == "POST":
# #         data = json.loads(request.body)  # parse JSON manually
# #         is_active = data.get("active")
# #         rule = LogicController.objects.get(id=rule_id)
# #         rule.active = is_active
# #         rule.save()
# #         return JsonResponse({"success": True, "active": rule.active})
# #     return JsonResponse({"error": "Invalid request"}, status=400)
# @require_POST
# # @ensure_csrf_cookie
# def toggle_logic_active(request, pk):
#     is_active = request.POST.get("active") == "true"
#     rule = LogicController.objects.get(id=pk)
#     rule.active = is_active
#     rule.save()
#     return JsonResponse({"success": True, "active": rule.active})


@require_POST
def toggle_logic_active(request, pk):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    is_active = data.get('active')
    if not isinstance(is_active, bool):
        # if the client sends strings, you could accept 'true'/'false' also
        return JsonResponse({'success': False, 'error': 'Invalid active value'}, status=400)

    try:
        rule = LogicController.objects.get(pk=pk)
    except LogicController.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)

    rule.active = is_active
    rule.save()
    return JsonResponse({'success': True, 'active': rule.active})


def delete_logic_rule_view(request, pk):
    logic_rule = get_object_or_404(LogicController, pk=pk)

    if request.method == 'POST':
        logic_rule.delete()
        return redirect('devices:details')

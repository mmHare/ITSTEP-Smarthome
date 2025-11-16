import csv
import io
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

from stats.models import StatsDeviceState, StatsUserAction


def stats_home_view(request):
    user_name = request.user.username

    if not user_name:
        return redirect('smarthome:login')


def export_view(request, mode, pk=None):
    user = request.user

    if not user.username:
        return redirect('smarthome:login')

    try:
        if mode == "user":  # get data for current user
            file_name = f'export-{user.username}'
            # list of model field names
            fields = [f.name for f in StatsUserAction._meta.get_fields()
                      if f.concrete and (not f.is_relation or f.many_to_one)]
            log_records = StatsUserAction.objects.filter(
                user=user).values(*fields)
            # *fields - unpack list (.values doesn't accept list)

        elif mode == "all-users":  # get data for all users
            file_name = 'export-users'
            fields = [f.name for f in StatsUserAction._meta.get_fields()
                      if f.concrete and (not f.is_relation or f.many_to_one)]
            log_records = StatsUserAction.objects.filter().values(*fields)

        elif mode == "device":  # get data for given device
            if pk <= 0:
                raise ValueError("Invalid device id")
            else:
                file_name = f'export-device-{pk}'
                fields = [f.name for f in StatsDeviceState._meta.get_fields()
                          if f.concrete and (not f.is_relation or f.many_to_one)]
                log_records = StatsDeviceState.objects.filter(
                    device_id=pk).values(*fields)

        elif mode == "all-devices":
            file_name = f'export-devices'
            fields = [f.name for f in StatsDeviceState._meta.get_fields()
                      if f.concrete and (not f.is_relation or f.many_to_one)]
            log_records = StatsDeviceState.objects.filter().values(*fields)

        else:
            raise ValueError("Invalid export mode")
    except Exception as e:
        return HttpResponseBadRequest(f"Export error: {e}")

    try:
        # convert data to CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(log_records)
        content = output.getvalue()

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={file_name}.csv'

    except Exception as e:
        return HttpResponse(f"Error preparing export: {e}", status=500)

    return response

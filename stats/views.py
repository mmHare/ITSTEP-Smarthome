import csv
import io
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from stats.models import StatsDeviceState, StatsUserAction
from stats.stats_service import StatsService


def stats_home_view(request):
    user = request.user

    if not user.username:
        return redirect('smarthome:login')

    if user.is_staff:
        user_logs = StatsUserAction.objects.filter().order_by("-timestamp").values("timestamp", "user", "user_action",
                                                                                   "item_kind", "item_id", "item_name")
    else:
        user_logs = StatsUserAction.objects.filter(user=user).order_by("-timestamp").values("timestamp", "user", "user_action",
                                                                                            "item_kind", "item_id", "item_name")

    # pagination
    paginator = Paginator(user_logs, 8)
    page_number = request.GET.get("page")
    page_log = paginator.get_page(page_number)

    return render(request, 'stats/home.html', {
        'user_name': user.username,
        'page_log': page_log})


def stats_sort_view(request, mode):
    user = request.user

    if not user.username:
        return redirect('smarthome:login')

    if user.is_staff:
        user_logs = StatsUserAction.objects.filter().order_by(mode).values("timestamp", "user", "user_action",
                                                                           "item_kind", "item_id", "item_name")
    else:
        user_logs = StatsUserAction.objects.filter(user=user).order_by(mode).values("timestamp", "user", "user_action",
                                                                                    "item_kind", "item_id", "item_name")

    # pagination
    paginator = Paginator(user_logs, 8)
    page_number = request.GET.get("page")
    page_log = paginator.get_page(page_number)

    return render(request, 'stats/home.html', {
        'user_name': user.username,
        'page_log': page_log})


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


def clear_log_view(request, mode, pk=None):
    try:
        if mode == "user":  # get data for current user
            StatsService.clear_user_logs(request.user)
            return HttpResponse("Clear user history success.", status=200)

        elif mode == "all-users":  # get data for all users
            StatsService.clear_user_logs()
            return HttpResponse("Clear users history success.", status=200)

        elif mode == "device":  # get data for given device
            if pk <= 0:
                raise ValueError("Invalid device id")
            else:
                StatsService.clear_device_logs(pk)
                return HttpResponse("Clear device history success.", status=200)

        elif mode == "all-devices":
            StatsService.clear_device_logs(pk)
            return HttpResponse("Clear device history success.", status=200)
    except Exception as e:
        return HttpResponseBadRequest(f"Clear history error: {e}")

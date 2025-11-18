import csv
import io
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from stats.models import StatsUserAction


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




def export_view(request, mode):
    user = request.user

    if not user.username:
        return redirect('smarthome:login')

    if mode == "user":
        # get data for current user
        file_name = f'export-{user.username}'
        log_records = StatsUserAction.objects.filter(user=user).values("timestamp", "user", "user_action",
                                                                       "item_kind", "item_id", "item_name")
    elif mode == "all-users":
        # get data for all users
        file_name = 'export-users'
        log_records = StatsUserAction.objects.filter().values("timestamp", "user", "user_action",
                                                              "item_kind", "item_id", "item_name")

    # convert data
    output = io.StringIO()
    fields = ["timestamp", "user", "user_action",
              "item_kind", "item_id", "item_name"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(log_records)
    content = output.getvalue()

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file_name}.csv'

    return response

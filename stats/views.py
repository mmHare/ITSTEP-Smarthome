from django.shortcuts import redirect, render


def stats_home_view(request):
    user_name = request.user.username

    if not user_name:
        return redirect('smarthome:login')

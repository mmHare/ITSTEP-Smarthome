from django.shortcuts import redirect, render


def devices_home_view(request):
    user_name = request.user.username

    if not user_name:
        return redirect('smarthome:login')

    return render(request, 'devices/home.html', {'user_name': user_name})

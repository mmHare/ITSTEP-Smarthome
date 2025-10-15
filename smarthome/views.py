from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import generic

from .models import HomeUser


# class IndexView(generic.ListView):
#     template_name = "smarthome/index.html"
#     context_object_name = "home_users_list"

#     def get_queryset(self):
#         # """Return the last five published questions."""
#         return HomeUser.objects.order_by("-user_name")


# class DetailView(generic.DetailView):
#     model = HomeUser
#     template_name = "smarthome/detail.html"


def index_view(request):
    # smart root - <a href="{% url 'smarthome:index' %}">SmartHome</a>
    # Check if user info is in session
    if request.session.get('user_name'):
        return redirect('smarthome:home')
    else:
        return redirect('smarthome:login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = HomeUser.objects.get(
                user_name=username, user_password=password)
            # Save user info in session
            request.session['user_id'] = user.id
            request.session['user_name'] = user.user_name
            return redirect('smarthome:home')  # ✅ namespaced redirect
        except HomeUser.DoesNotExist:
            return render(request, 'smarthome/login.html', {'error': 'Invalid username or password'})

    return render(request, 'smarthome/login.html')


def home_view(request):
    user_name = request.session.get('user_name')

    if not user_name:
        return redirect('smarthome:login')  # ✅ namespaced redirect

    return render(request, 'smarthome/home.html', {'user_name': user_name})


def logout_view(request):
    request.session.flush()
    return redirect('smarthome:login')  # ✅ namespaced redirect

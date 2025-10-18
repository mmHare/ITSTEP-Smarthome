from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm

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
    if request.user.username:
        return redirect('smarthome:home')
    else:
        return redirect('smarthome:login')


def home_view(request):
    user_name = request.user.username

    if not user_name:
        return redirect('smarthome:login')  # ✅ namespaced redirect

    return render(request, 'smarthome/home.html', {'user_name': user_name})


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             user = HomeUser.objects.get(
#                 user_name=username, user_password=password)
#             # Save user info in session
#             request.session['user_id'] = user.id
#             request.session['user_name'] = user.user_name
#             return redirect('smarthome:home')  # ✅ namespaced redirect
#         except HomeUser.DoesNotExist:
#             return render(request, 'smarthome/login.html', {'error': 'Invalid username or password'})

#     return render(request, 'smarthome/login.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('smarthome:home')
    else:
        form = AuthenticationForm()
        # return render(request, 'smarthome/login.html', {'form': form, 'error': 'Invalid username or password'})
    return render(request, 'smarthome/login.html', {'form': form})


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('smarthome:login')  # ✅ namespaced redirect


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('smarthome:login')
        print('not valid')
    else:
        form = SignUpForm()
    return render(request, 'smarthome/register.html', {'form': form})

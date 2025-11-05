from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignUpForm


def index_view(request):
    if request.user.username:
        return redirect('smarthome:home')
    else:
        return redirect('smarthome:login')


def home_view(request):
    user_name = request.user.username

    if not user_name:
        return redirect('smarthome:login')
    return render(request, 'smarthome/home.html', {'user_name': user_name})


def homepage_view(request):
    return render(request, 'smarthome/homepage.html')

def about_view(request):
    return render(request, 'smarthome/about.html')


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
    return render(request, 'smarthome/login.html', {'form': form})


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('smarthome:login')


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

from django.urls import path
from .views import *

app_name = "smarthome"
urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]

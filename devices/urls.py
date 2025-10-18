from django.urls import path
from . import views

app_name = "devices"
urlpatterns = [
    path('', views.devices_home_view, name='devices_home'),
]

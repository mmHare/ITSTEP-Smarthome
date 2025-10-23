from django.urls import path
from .views import *

app_name = "devices"
urlpatterns = [
    path('', devices_home_view, name='home'),
    path('new/', new_device_view, name='new_device'),
    path('<int:pk>/', DetailView.as_view(), name='details'),
    path('<int:pk>/edit/', DeviceUpdateView.as_view(), name='edit_device'),
    path('<int:pk>/delete/', delete_device_view, name='delete_device'),
    path('rooms/', room_list_view, name='room_list'),
    path('rooms/<int:pk>/delete/', delete_device_view, name='delete_room'),
]

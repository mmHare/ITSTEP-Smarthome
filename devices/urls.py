from django.urls import path
from . import views

app_name = "devices"
urlpatterns = [
    path('', views.devices_home_view, name='home'),
    path('new/', views.new_device_view, name='new_device'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
    path('<int:pk>/edit/', views.DeviceUpdateView.as_view(), name='edit_device'),
    path('<int:pk>/delete/', views.delete_device_view, name='delete_device'),
]

from django.urls import path
from .views import *

app_name = "devices"
urlpatterns = [
    path('', devices_home_view, name='home'),
    path('new/', new_device_view, name='new_device'),
    path('<int:pk>/new/', new_rule_view, name='new_rule'),
    path('<int:pk>/', DeviceDetailView.as_view(), name='details'),
    path('<int:pk>/edit/', DeviceUpdateView.as_view(), name='edit_device'),
    path('<int:pk>/delete/', delete_device_view, name='delete_device'),
    # path('<int:pk>/edit-rule/', RuleUpdateView.as_view(), name='edit_rule'),
    path('rooms/', room_list_view, name='room_list'),
    path('rooms/<int:pk>/delete/', delete_room_view, name='delete_room'),
    path('logic/<int:pk>/toggle-active/',
         toggle_logic_active, name='toggle_logic_active'),
    path('logic/<int:pk>/rule-action/', rule_action, name='rule_action'),
]

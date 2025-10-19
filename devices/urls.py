from django.urls import path
from . import views

app_name = "devices"
urlpatterns = [
    path('', views.devices_home_view, name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
]

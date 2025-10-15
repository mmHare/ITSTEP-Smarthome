from django.urls import path
from . import views

app_name = "smarthome"
urlpatterns = [
    path('', views.index_view, name='index'),   # ✅ Root redirect
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
]

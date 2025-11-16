from django.urls import path

from stats.views import export_view, stats_home_view


app_name = "stats"
urlpatterns = [
    path('', stats_home_view, name='home'),
    path('export/<str:mode>/', export_view, name='export'),
    path('export/<str:mode>/<int:pk>/', export_view, name='export')
]

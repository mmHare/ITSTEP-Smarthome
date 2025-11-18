from django.urls import path

from stats.views import export_view, stats_home_view, stats_sort_view, clear_log_view


app_name = "stats"
urlpatterns = [
    path('', stats_home_view, name='home'),
    path('sort/<str:mode>/', stats_sort_view, name='sort'),
    path('export/<str:mode>/', export_view, name='export'),
    path('export/<str:mode>/<int:pk>/', export_view, name='export'),
    path('clear-logs/<str:mode>/', clear_log_view, name='clear-logs'),
    path('clear-logs/<str:mode>/<int:pk>/', clear_log_view, name='clear-logs'),
]

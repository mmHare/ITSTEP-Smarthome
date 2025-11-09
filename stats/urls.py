from django.urls import path

from stats.views import stats_home_view


app_name = "stats"
urlpatterns = [
    path('', stats_home_view, name='home'),
]

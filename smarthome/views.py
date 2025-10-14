from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import HomeUser


# def index(request):
#     return HttpResponse("Yo, this is SmartHome index.")


class IndexView(generic.ListView):
    template_name = "smarthome/index.html"
    context_object_name = "home_users_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return HomeUser.objects.order_by("-user_name")


class DetailView(generic.DetailView):
    model = HomeUser
    template_name = "smarthome/detail.html"

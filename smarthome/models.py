from django.db import models


class HomeUser(models.Model):
    user_name = models.CharField("name", unique=True, max_length=200)
    user_password = models.CharField("password", max_length=50)

    def __str__(self):
        return self.user_name


class Device(models.Model):
    device_name = models.CharField("name", max_length=200)
    user = models.ForeignKey(HomeUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.device_name

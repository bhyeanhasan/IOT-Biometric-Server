from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    PSTU_ID = models.CharField(max_length=50)
    session = models.CharField(max_length=50)
    fingerprint = models.CharField(max_length=10)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Machine(models.Model):
    machineId = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    state = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name

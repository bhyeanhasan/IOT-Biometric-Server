from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50)
    PSTU_ID = models.CharField(max_length=50)
    session = models.CharField(max_length=50)
    fingerprint = models.CharField(max_length=10)
    balance = models.IntegerField()

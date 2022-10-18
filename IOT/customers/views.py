from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer


def index(request):
    customer = Customer.objects.all()
    return render(request, 'index.html', {'customer': customer})


def customers(request,fingerprint):
    customer = Customer.objects.get(fingerprint=fingerprint)
    customer.balance = customer.balance-50;
    customer.save()
    return render(request, 'profile.html', {'obj': customer})

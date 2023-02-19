from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Customer, Machine


def index(request):
    customer = Customer.objects.all()
    return render(request, 'index.html', {'customer': customer})


def customers(request, fingerprint):
    customer = Customer.objects.get(fingerprint=fingerprint)
    customer.balance = customer.balance - 50
    customer.save()

    machine = Machine.objects.get(machineId=0)
    machine.state = 1
    machine.save()
    return JsonResponse({'Name': customer.name, 'Balance': customer.balance, 'Machine State': machine.state,
                         'Status': 'Poring Coffee ....', })


def machineStatusCheck(request):
    machine = Machine.objects.get(machineId=0)
    state = machine.state
    return JsonResponse({'state':state})


def pourCofee(request, machineId):
    machine = Machine.objects.get(machineId=machineId)
    machine.state = 0
    machine.save()
    return JsonResponse({'Machine State': machine.state, 'Status': 'Poring Coffee Done'})

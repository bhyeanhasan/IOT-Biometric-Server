from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Customer, Machine, Order
from django.core.cache import cache # This is the memcache cache.


def index(request):
    customer = Customer.objects.all()
    return render(request, 'index.html', {'customer': customer})


def customers(request, fingerprint):
    customer = Customer.objects.get(fingerprint=fingerprint)
    if customer.balance > 50:
        customer.balance = customer.balance - 50
        customer.save()
    else:
        return redirect('/')

    machine = Machine.objects.get(machineId=0)
    machine.state = 1
    machine.save()

    order = Order()
    order.customer = customer
    order.time = datetime.now()
    order.save()

    return JsonResponse({'Name': customer.name, 'Balance': customer.balance, 'Machine State': machine.state,
                         'Status': 'Poring Coffee ....', })


def machineStatusCheck(request):
    machine = Machine.objects.get(machineId=0)
    state = machine.state
    return JsonResponse({'state': state})


def pourCofee(request, machineId):
    machine = Machine.objects.get(machineId=machineId)
    machine.state = 0
    machine.save()
    return JsonResponse({'Machine State': machine.state, 'Status': 'Poring Coffee Done'})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'User not found')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.info(request, 'Password no matched')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=pass1)
            user.save()
            return redirect('login')

    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def profile(request):
    cache.clear()
    if request.method == 'GET':
        try:
            profile = Customer.objects.get(user=request.user)
            img = str(request.user.username) + '.bmp'
            return render(request, 'profile.html', {'profile': profile, 'img': img})
        except:
            profile = Customer(user=request.user)
            img = str(request.user.username) + '.bmp'
            profile.save()
            return render(request, 'profile.html', {'profile': profile, 'img': img})
    else:
        profile = Customer.objects.get(user=request.user)

        name = request.POST['name']
        PSTU_ID = request.POST['PSTU_ID']
        session = request.POST['session']

        profile.name = name
        profile.PSTU_ID = PSTU_ID
        profile.session = session

        profile.save()

        return redirect('profile')

from django.contrib import admin

from .models import Customer
from .models import Machine
from .models import Order

admin.site.register(Customer)
admin.site.register(Machine)
admin.site.register(Order)
from django.contrib import admin

from .models import Customer
from .models import Machine

admin.site.register(Customer)
admin.site.register(Machine)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/<int:fingerprint>/', views.customers),
    path('check/', views.machineStatusCheck),
    path('machine/<int:machineId>/', views.pourCofee),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='finger_index'),
    path('show', views.showAllPorts, name='showport'),
    path('read', views.takeFingerPrint, name='read'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='finger_index'),
    path('show', views.show, name='show'),
    path('read', views.takeFingerPrint, name='read'),
]

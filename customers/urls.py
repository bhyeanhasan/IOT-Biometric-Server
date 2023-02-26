from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/<int:fingerprint>/', views.customers),
    path('check/', views.machineStatusCheck),
    path('machine/<int:machineId>/', views.pourCofee),
    path('accounts/login/', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
]

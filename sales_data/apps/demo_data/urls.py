from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.demo_dashboard, name = 'demo_dashboard'),
    path('network', views.demo_network_traffic,     name = 'demo_network_traffic'),
]

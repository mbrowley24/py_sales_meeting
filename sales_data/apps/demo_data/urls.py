from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo_dashboard, name='demo_dashboard'),

]

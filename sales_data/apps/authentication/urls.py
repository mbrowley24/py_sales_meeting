from django.urls import path
from . import views

urlpatterns = [
    path('', views.app_login, name='login'),
]

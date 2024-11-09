from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_reps, name='sales_rep_table'),
]

from django.urls import path
from apps.customer.views import *

urlpatterns = [
    path('', CustomerTableView.as_view, name='customers'),
]

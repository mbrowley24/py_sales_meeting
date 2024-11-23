from django.urls import path
from apps.customer.views import *
from apps.customer.views import NewCustomerView

urlpatterns = [
    path('', CustomerTableView.as_view(), name = 'customers'),
    path('new/', NewCustomerView.as_view(),   name = 'new_customer'),
]

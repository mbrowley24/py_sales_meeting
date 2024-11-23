"""
URL configuration for sales_data project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.authentication.urls', 'sales_data'), namespace='apps.authentication')),
    path('appManagement/', include(('apps.Management.urls', 'sales_data'), namespace='apps.management')),
    path('appointments/', include(('apps.appointments.urls', 'sales_data'), namespace='apps.appointments')),
    path('customers/', include(('apps.customer.urls', 'sales_data'), namespace='apps.customer')),
    path('dashboard/', include(('apps.dashboard.urls', 'sales_data'), namespace='apps.dashboard')),
    path('sales_reps/', include(('apps.salesreps.urls', 'sales_data'), namespace='apps.sales_rep')),
]

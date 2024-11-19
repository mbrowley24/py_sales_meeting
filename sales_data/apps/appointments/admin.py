from django.contrib import admin
from .models import Appointment, AppointmentType, AppointmentProduct
admin.site.register(Appointment)
admin.site.register(AppointmentType)
admin.site.register(AppointmentProduct)


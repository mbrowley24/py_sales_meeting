from django.contrib import admin
from .models import Appointment, AppointmentType

admin.site.register(Appointment)
admin.site.register(AppointmentType)
    

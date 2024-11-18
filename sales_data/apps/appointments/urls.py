from django.urls import path
from apps.appointments.views import *

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment_list'),
    path('new', NewAppointmentView.as_view(), name='new_appointment'),
]

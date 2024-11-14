from django.db import models
from django.contrib.auth.models import User
from ..salesreps.models import SalesRepresentative



class AppointmentType(models.Model):

    class Meta:
        db_table = 'appointment_types'
        verbose_name = 'Appointment Type'
        verbose_name_plural = 'Appointment Types'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['public_id']),
        ]


    public_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Appointment(models.Model):

    class Meta:
        db_table = 'appointments'
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
        indexes = [
            models.Index(fields=['date'], name='date_index'),
            models.Index(fields=['public_id'], name='appointment_public_id_index'),
        ]


    public_id = models.CharField(max_length=100, unique=True)
    date = models.DateField(null=False, blank=False)
    title = models.CharField(max_length=100)
    type = models.ForeignKey(AppointmentType, on_delete=models.CASCADE, related_name='appointments')
    sales_engineer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    sales_representative = models.ForeignKey(SalesRepresentative, on_delete=models.CASCADE, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

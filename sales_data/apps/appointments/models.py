from apps.formData.models.products import Products
from django.db import models
from django.contrib.auth.models import User

from ..customer.models import Customer
from ..salesreps.models import SalesRepresentative



class AppointmentType(models.Model):

    class Meta:
        db_table            = 'appointment_types'
        verbose_name        = 'appointment type'
        verbose_name_plural = 'appointment types'
        indexes             = [
            models.Index(fields = ['name'], name='appointment_type_name'),
            models.Index(fields = ['public_id']),
        ]


    public_id   = models.CharField(max_length=100, unique=True)
    name        = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name.upper()


class Appointment(models.Model):

    class Meta:
        db_table            = 'appointments'
        verbose_name        = 'appointment'
        verbose_name_plural = 'appointments'
        indexes = [
            models.Index(fields = ['date'], name='appointment_date_index'),
            models.Index(fields = ['type'], name='appointment_type_index'),
            models.Index(fields = ['public_id'], name='appointment_public_id_index'),
            models.Index(fields = ['sales_engineer'], name='appointment_se_index'),
            models.Index(fields = ['sales_representative'], name='appointment_sales_rep_index'),
        ]


    public_id = models.CharField(max_length = 100,
                                 unique     = True
                                 )
    date                 = models.DateTimeField(null = False)
    title                = models.CharField(max_length = 100)
    notes                = models.TextField(max_length = 255,
                                            null       = True,
                                            blank      = True
                                            )
    type                 = models.ForeignKey(AppointmentType,
                                             on_delete    = models.CASCADE,
                                             related_name = 'appointments')
    customer             = models.ForeignKey(Customer,
                                             on_delete    = models.CASCADE,
                                             related_name = 'appointments'
                                             )
    sales_engineer       = models.ForeignKey(User,
                                             on_delete    = models.CASCADE,
                                             related_name ='appointments'
                                             )
    sales_representative = models.ForeignKey(SalesRepresentative,
                                             on_delete    = models.CASCADE,
                                             related_name ='appointments'
                                             )
    created_at           = models.DateTimeField(auto_now_add = True)
    updated_at           = models.DateTimeField(auto_now = True)


class AppointmentProduct(models.Model):
    class Meta:
        db_table            = 'appointment_products'
        verbose_name        = 'appointment product'
        verbose_name_plural = 'appointment products'
        indexes = [
            models.Index(
                fields = ['appointment'],
                name   = 'appointment_appointment_index'
            ),
            models.Index(
                fields = ['product'],
                name   = 'appointment_product_index'
            ),
        ]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='products')
    product     = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='appointments')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
from apps.salesreps.models import SalesRoles
from apps.appointments.models import AppointmentType
from apps.formData.models.timezone import Timezone
from apps.formData.models.products import Products
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import os
from .helper_functions import start_data
from utils.helper import generate_public_id

#Create sales roles to identify the sale rep roles
def create_sales_roles():
    roles = {
        'eae': 'enterprise sales rep',
        'eam': 'enterprise account rep',
        'sbs': 'small business services'
    }

    for key, value in roles.items():

        try:

            SalesRoles.objects.get(name = key)

            # if user exists continue to next
            continue

        except SalesRoles.DoesNotExist:
            data = {
                "public_id": generate_public_id(SalesRoles),
                "name": key,
                'description': value,
            }

            SalesRoles.objects.create(**data)

#appointment type of appointment assigned to appointments
def create_appointment_type():
    types = {
        "pa" : "proposal appointment",
        "fa" : "follow-up appointment",
        "iah": 'initial appointment held',
    }

    for key, value in types.items():

        try:


            AppointmentType.objects.get(name = key)

            continue
        except AppointmentType.DoesNotExist:

            fields={
                'public_id' : generate_public_id(AppointmentType),
                'name' : key,
                'description' : value,
            }
            AppointmentType.objects.create(**fields)


#creates products
def create_products():

    file_path = os.path.join(settings.BASE_DIR, 'static/data/products.txt')

    try:
        file = open(file_path, 'r')

        for line in file:

            parts = line.lower().strip().split('/')

            try:

                Products.objects.get(name=parts[0])
                continue
            except Products.DoesNotExist:

                Products.objects.create(
                    public_id   = generate_public_id(Products),
                    name        = parts[0],
                    description = parts[1],
                )

    except FileNotFoundError:
        print("File doesn't exist")



#Creates timezones that are assigned to sales engineers, manager, and sales reps
def create_timezone():
    timezones = ['America / New_York', 'America / Chicago',
                 'America / Denver', 'America / Los_Angeles',
                 'America / Anchorage', 'Pacific/Honolulu',
                 ]



    for timezone in timezones:

        try:

            Timezone.objects.get(name=timezone)
            continue

        except Timezone.DoesNotExist:

            public_id = generate_public_id(Timezone)
            Timezone.objects.create(
                name=timezone,
                public_id = public_id
            )




class Command(BaseCommand):
    help = 'Create a sales roles'

    def handle(self, *args, **options):

        # Create a user
        create_appointment_type()
        create_products()
        create_sales_roles()
        create_timezone()
        start_data()


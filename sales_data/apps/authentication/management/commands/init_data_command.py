from django.core.management.base import BaseCommand, CommandError
from apps.salesreps.models import SalesRoles
from apps.appointmenttracker.models import AppointmentType
from utils.helper import generate_public_id


def create_sales_roles():
    roles = {
        'eae': 'enterprise sales rep',
        'eam': 'enterprise account rep',
        'sbs': 'small business services'
    }

    for key, value in roles.items():

        try:

            SalesRoles.objects.get(name=key)

            # if user exists continue to next
            continue

        except SalesRoles.DoesNotExist:
            data = {
                "public_id": generate_public_id(SalesRoles),
                "name": key,
                'description': value,
            }

            SalesRoles.objects.create(**data)


def create_appointment_type():
    types = {
        "pa" : "proposal appointment",
        "fa" : "follow-up appointment",
        "iah": 'initial appointment held',
    }

    for key, value in types.items():

        try:


            AppointmentType.objects.get(name=key)
            continue
        except AppointmentType.DoesNotExist:

            fields={
                'public_id' : generate_public_id(AppointmentType),
                'name' : key,
                'description' : value,
            }
            AppointmentType.objects.create(**fields)



class Command(BaseCommand):
    help = 'Create a sales roles'

    def handle(self, *args, **options):

        # Create a user
        create_sales_roles()
        create_appointment_type()

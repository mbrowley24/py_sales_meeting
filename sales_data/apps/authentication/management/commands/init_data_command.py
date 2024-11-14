from django.core.management.base import BaseCommand, CommandError
from apps.salesreps.models import SalesRoles
from apps.appointmenttracker.models import AppointmentType
from utils.helper import generate_public_id
from apps.formData.models.timezone import Timezone
from apps.formData.models.division import Division, Region

#Create sales roles to identify the sale rep roles
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

#appointment type of appointment assigned to appointments
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


#create regions and division for sales engineers and managers
def create_divisions_regions():
    divisions = {
        'west' : [{'name':'california', 'abbr':'ca'},
                  {'name':'pacific north west', 'abbr':'pnr'},
                  {'name':'mountain west', 'abbr':'mwr'},]
    }

    for key, value in divisions.items():
        division = None

        try:
            division = Division.objects.get(name=key)

        except Division.DoesNotExist:

            division = Division.objects.create(
                public_id=generate_public_id(Division),
                name=key,
                description="",
            )

        if division is None:
            continue

        for region in value:

            try:

                region = Region.objects.get(
                    name=region['name'],
                    abbreviation=region['abbr']
                )
                if region.public_id == '':
                    region.public_id = generate_public_id(Region)
                    region.save()
                continue

            except Region.DoesNotExist:

                Region.objects.create(
                    public_id=generate_public_id(Region),
                    name=region['name'],
                    abbreviation=region['abbr'],
                    division=division
                )


class Command(BaseCommand):
    help = 'Create a sales roles'

    def handle(self, *args, **options):

        # Create a user
        create_sales_roles()
        create_appointment_type()
        create_timezone()
        create_divisions_regions()

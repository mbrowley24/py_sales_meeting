from apps.authentication.models import UserProfile
from apps.salesreps.models import SalesRepresentative, SalesRoles
from apps.formData.models.timezone import Timezone
from apps.formData.models.division import Region
from apps.formData.models.Vertical import Vertical

from datetime import time
from django.contrib.auth.models import User, Group
from faker import Faker
import os
import random
from utils.helper import generate_public_id




def create_user():
    faker = Faker()

    first_name = faker.first_name().lower()
    last_name = faker.last_name().lower()
    username = f'{first_name[0]}{last_name}'

    final_username = username

    # check if the username is in use. if in use generate another username
    while User.objects.filter(username=final_username).exists():
        final_username = f'{username}{random.randint(1, 999)}'

    email = f'{final_username}@sellcrew.com'

    manager = User.objects.create_user(
        username=final_username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=faker.password(),
        is_active=False,
        is_staff=False,
        is_superuser=False,
    )

    sales_timezones = Timezone.objects.get(name = "America / Denver")
    region          = Region.objects.get(name = 'mountain west')
    public_id       = generate_public_id(UserProfile)

    UserProfile.objects.create(
        public_id = public_id,
        user      = manager,
        time_zone = sales_timezones,
        region    = region,

    )


    return manager

def create_sales_representative(sales_engineer):
    faker = Faker()

    sales_rep_count = sales_engineer.sales_reps.count()

    #if sales rep count greater than 5
    if sales_rep_count > 5:
        return None

    eae_count = (SalesRepresentative.objects
                     .filter(sales_engineer = sales_engineer)
                     .filter('eae')
                     .count())

    eam_count = (SalesRepresentative.objects
                        .filter(sales_engineer = sales_engineer)
                        .filter('eam')
                        .count())

    sbs_count = (SalesRepresentative.objects
                     .filter(sales_engineer = sales_engineer)
                     .filter('sbs')
                     .count())

    while (eae_count + sbs_count + eam_count) < 6:

        public_id  = generate_public_id(SalesRepresentative)
        first_name = faker.first_name().lower()
        last_name  = faker.last_name().lower()
        email      = f'{first_name[0]}{last_name}@sellcrew.com'
        role       = None

        #modify password if email exists
        while SalesRepresentative.objects.filter(email = email).exists():
            email = f'{first_name[0]}{last_name}{random.randint(1, 999)}@sellcrew.com'


        if eae_count < 2:
            role = SalesRoles.objects.get("eae")
            new_eae = SalesRepresentative.objects.create(
                public_id      = public_id,
                first_name     = first_name,
                last_name      = last_name,
                email          = email,
                role           = role,
                quota          = 4200,
                sales_engineer = sales_engineer,
            )


        if eam_count < 2:
            role = SalesRoles.objects.get("eam")
            eam = SalesRepresentative.objects.create(
                public_id      = public_id,
                first_name     = first_name,
                last_name      = last_name,
                email          = email,
                role           = role,
                quota          = 1750,
                sales_engineer = sales_engineer,
            )


        if sbs_count < 2:
            role = SalesRoles.objects.get("sbs")
            sbs = SalesRepresentative.objects.create(
                public_id      = public_id,
                first_name     = first_name,
                last_name      = last_name,
                email          = email,
                role           = role,
                quota          = 2400,
                sales_engineer = sales_engineer,
            )


            eae_count = (SalesRepresentative.objects
                         .filter(sales_engineer=sales_engineer)
                         .filter('eae')
                         .count())

            eam_count = (SalesRepresentative.objects
                         .filter(sales_engineer=sales_engineer)
                         .filter('eam')
                         .count())

            sbs_count = (SalesRepresentative.objects
                         .filter(sales_engineer=sales_engineer)
                         .filter('sbs')
                         .count())



def get_create_group(group_name):

    try:

        return Group.objects.get(name = group_name)

    except Group.DoesNotExist:
        return Group.objects.create(name = group_name)


def create_dummy_sales_managers():

    dummy_sales_managers_count = User.objects.filter(groups__name='dummy se mgmt').count()

    if dummy_sales_managers_count > 3:
        print("skip")
        return

    for _ in range(5):

        sales_manager = create_user()

        group = get_create_group('dummy se mgmt')

        sales_manager.groups.add(group)
        sales_manager.save()



def create_dummy_se_account():
    faker = Faker()

    dummy_managers = User.objects.filter(groups__name = 'dummy se mgmt')

    for manager in dummy_managers:

        #if manager has more than 5 reps skip
        if manager.sales_engineers.count() > 5:
            continue

        sales_engineer = create_user()

        public_id = generate_public_id(SalesRepresentative)
        sales_timezones = Timezone.objects.get(name="America / Denver")
        region = Region.objects.get(name='mountain west')

        UserProfile.objects.create(
            public_id = public_id,
            user      = sales_engineer,
            manager   = manager,
            time_zone = sales_timezones,
            region    = region,
        )


        group = get_create_group('dummy se')

        sales_engineer.managers.add(manager)
        sales_engineer.groups.add(group)

        sales_engineer.save()

        create_sales_representative(sales_engineer)




def create_sales_appointment(sales_engineer):
    faker       = Faker()
    random_date = faker.date_between(start_date= '-3y', end_date= '+3y' )
    hour        = random.randint(0, 23)
    minute      = random.randint(0, 59)

    random_time = time(hour   = hour,
                       minute = minute
                       )



def create_verticals():
    # Get the current file's directory
    current_folder = os.path.dirname(__file__)
    file_path      = os.path.join(current_folder, 'vertical.txt')

    try:
        with open(file_path, 'r') as file:

            for line in file:
                text = line.lower().strip().split(':')

                try:
                    Vertical.objects.get(name = text[0])

                    continue
                except Vertical.DoesNotExist:
                    Vertical.objects.create(
                        public_id = generate_public_id(Vertical),
                        name = text[0],
                        description = text[1],
                    )

    except FileNotFoundError as  e:
        print(e)
        return None

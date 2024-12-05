from random import random



from apps.formData.models.timezone import Timezone
from apps.demo_data.models import (TestSalesRepresentative, TestSalesEngineer, TestGroup, TestAppointment,
                                   TestCustomer, TestOrganization, TestSalesEngineerManager, TestAppointmentType)
from datetime import time
from faker import Faker
import os
import json
from apps.formData.models.timezone import Timezone
from apps.salesreps.views import sales_reps
from utils.helper import generate_public_id, generate_random_string



def random_time():

    #fake data generator
    fake = Faker()

    #days allow in timezone
    allowed_days = [0, 1, 2, 3, 4]  # Monday, Tuesday, Wednesday, Thursday, Friday

    #set start and end date variables
    start_time = (8, 0)  # 8:00 AM
    end_time = (17, 0)  # 5:00 PM

    #generate date and time
    while True:

        #dates between the current time and three years in the past
        random_date_time = fake.date_time_between(start_date='-3y', end_date='now')

        if random_date_time.weekday() in allowed_days:

            if start_time <= (random_date_time.hour, random_date_time.minute) <= end_time:

                return random_date_time


def create_organization(name):

    # organization container
    try:
        # check if the organization exists
        organization = TestOrganization.objects.get(name = name)

        return organization

    except TestOrganization.DoesNotExist:

        # create if it doesn't exist
        return TestOrganization.objects.create(
            public_id  = generate_public_id(TestOrganization),
            name       = name
        )

def create_sales_groups(groups, organization):
    # generate groups from json and append to list to recall later
    groups = []
    for group in groups:

        try:

            test_group = TestGroup.objects.get(
                name = group,
                organization = organization
            )

            groups.append(test_group)

        except TestGroup.DoesNotExist:

            test_group = TestGroup.objects.create(
                public_id    = generate_public_id(TestGroup),
                name         = group["name"],
                description  = group["description"],
                organization = organization,
            )

            groups.append(test_group)


    return groups


#create sales reps companies and appointments
def create_sales_representatives(rep, sales_engineer, role):

    sales_rep = None

    try:

         return TestSalesRepresentative.objects.get(email = rep.email)

    except TestSalesRepresentative.DoesNotExist:

        return TestSalesRepresentative.objects.get(
                   public_id      = generate_public_id(TestSalesRepresentative),
                   first_name     = rep.first_name,
                   last_name      = rep.last_name,
                   email          = rep.email,
                   sales_engineer = sales_engineer,
                   quota          = rep.quota,
                   role           = role
        )



#creates sales engineer, sales reps and appointments
def create_sales_engineer(sales_manager,
                          sales_engineer,
                          timezone,
                          organization,
                          groups):

    sales_engineer_obj = None
    sales_engineer_group = [group.name == "sales engineers" for group in groups]

    try:

        sales_engineer_obj = TestSalesEngineer.objects.get(email = sales_engineer.email)

    except TestSalesEngineer.DoesNotExist:

        #create the sales engineer
        sales_engineer_obj = TestSalesEngineer.objects.create(

            first_name = sales_manager.first_name,
            last_name  = sales_manager.last_name,
            email      = sales_manager.email,
        )

        #create the user group
        TestGroup.objects.create(
            user  = sales_engineer_obj,
            group = sales_engineer_group,
        )

    sbs_group = [group.name == 'sbs' for group in groups][0]
    for new_sales_rep in sales_engineer.sbs:

        create_sales_representatives(new_sales_rep, sales_engineer, sbs_group)


    eae_group = [group.name == 'eae' for group in groups][0]
    for new_sales_role in sales_engineer.eae:

        create_sales_representatives(new_sales_role, sales_engineer, eae_group)


    eam_group = [group.name == 'eam' for group in groups][0]
    for new_sales_role in sales_engineer.eam:

        create_sales_representatives(new_sales_role, sales_engineer, eam_group)


#create sales manager, sales_engineer, sales reps and meetings
def create_sales_manager(sales_manager, organization, timezones, groups):

    sales_manager_obj = None

    timezone          = [sales_manager['timezone'] == x.name for x in timezones][0]

    sales_manager     = [group.name == "sales engineer managers" for group in groups][0]

    # check if timezone is in timezone if not skip sales_manager
    if timezone is None:
        return None

    username           = sales_manager['email'].split('@')[0]

    try:

        sales_manager_obj = TestSalesEngineerManager.objects.get( email = sales_manager['email'] )

    except TestSalesEngineerManager.DoesNotExist:

        #create a new sales manager
        sales_manager_obj = TestSalesEngineerManager(
            first_name    = sales_manager['first_name'],
            last_name     = sales_manager['first_name'],
            username      = username,
            email         = sales_manager['email'],
            is_superuser  = False,
            is_staff      = False,
            is_active     = False,
        )


        #attach the sales manager to user group entity
        TestGroup.objects.create(
            user  = sales_manager,
            group = sales_manager,
        )


    for sales_engineer in sales_manager.sales_engineers:

        create_sales_engineer(sales_manager_obj, sales_engineer, timezone, organization, groups)


    return sales_manager


def get_sales_manager_group(groups):

    sales_manager = [group.name == "sales engineer managers" for group in groups]

    if len(sales_manager) != 1:
        return None

    return sales_manager[0]

def start_data():


    #generate file path
    file_name             = "fake_data.json"
    current_directory     = os.path.dirname(os.path.abspath(__file__))
    folder                = f"{current_directory}/{file_name}"
    timezones             = Timezone.objects.all()
    appointment_types      = TestAppointmentType.objects.all()

    #open file and load to json to create the sample data from the web application
    with open(folder, 'r') as file:
        data          = json.load(file)

        #get or create organization
        organization  = create_organization(data['organization'])

        #get or create groups for dummy organization
        groups        = create_sales_groups(data['groups'], organization)



from apps.demo_data.models import TestSalesRepresentative, TestSalesEngineer, TestSalesEngineerManager
from django.db.models import Q
import re

# checks username or email exists. has_username applies to sales engineer managers and sales engineers
# else email is check for sales representative
def data_exists(data, has_username = True):

    if has_username:

        sales_manager_email_exists = TestSalesEngineerManager.objects.filter(
            Q(email = data['email']) | Q(username = data['username'])
        ).exists()

        sales_engineer_email_exists = TestSalesEngineer.objects.filter(
            Q(email = data['email']) | Q(username = data['username'])
        ).exists()

        sales_rep_email_exists = TestSalesRepresentative.objects.filter(email = data['email']).exists()

        return sales_manager_email_exists or sales_engineer_email_exists or sales_rep_email_exists

    else:

        sales_manager_email_exists = TestSalesEngineerManager.objects.filter(email = data['email']).exists()
        sales_engineer_email_exists = TestSalesEngineer.objects.filter(email = data['email']).exists()
        sales_rep_email_exists = TestSalesRepresentative.objects.filter(email = data['email']).exists()

        return sales_manager_email_exists or sales_engineer_email_exists or sales_rep_email_exists

# creates userdata has_username is for test sales engineer manager and test sales engineer entities
def generate_unique_user_data(faker, org_name, has_username = True):

    organization = re.sub(r'\s+', '', org_name)

    if has_username:

        first_name = faker.first_name().lower()
        last_name  = faker.last_name().lower()
        email      = f'{first_name}.{last_name}@{organization}.com'
        username   = f'{first_name[0]}{last_name}'

        return {
            'first_name' : first_name,
            'last_name'  : last_name,
            'email'      : email,
            'username'   : username
        }

    else:

        first_name = faker.first_name().lower()
        last_name  = faker.last_name().lower()
        email      = f'{first_name}{last_name}@{organization}.com'

        return {
            'first_name' : first_name,
            'last_name'  : last_name,
            'email'      : email
        }
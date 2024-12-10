from apps.demo_data.models import (TestSalesRepresentative, TestSalesEngineer, TestGroup, TestAppointment, TestCustomer,
                                   TestOrganization, TestSalesEngineerManager, TestSalesEngineerManagerGroup,
                                   TestAppointmentType, TestSalesEngineerGroup, TestSalesRole, TestVertical)

from utils.helper import generate_public_id
from .generate_user_data import generate_unique_user_data



#create sales manager, sales_engineer, sales reps and meetings
def create_sales_engineer_manager(organization_obj, faker):

    sales_engineer_managers = list(TestSalesEngineerManager.objects.filter(organization = organization_obj))

    if len(sales_engineer_managers) > 5:
        return sales_engineer_managers

    range_count = 6 - len(sales_engineer_managers)

    for _ in range(range_count):

        #generate unique data
        data                   = generate_unique_user_data(faker, organization_obj.name, True)

        public_id              = generate_public_id(TestSalesEngineerManager)

        sales_engineer_manager = TestSalesEngineerManager.objects.create(

            public_id    = public_id,
            first_name   = data['first_name'],
            last_name    = data['last_name'],
            email        = data['email'],
            organization = organization_obj,
            username     = data['username'],

        )

        sales_engineer_managers.append(sales_engineer_manager)


    return sales_engineer_managers


#group sales engineer managers to sales engineer manager group and checks for duplicate
def sales_engineer_managers_group(se_managers, group):

    for se_manager in se_managers:

        if not TestSalesEngineerManagerGroup.objects.filter(group = group, sales_manager = se_manager ).exists():
            TestSalesEngineerManagerGroup.objects.create(
                group         = group,
                sales_manager = se_manager
            )
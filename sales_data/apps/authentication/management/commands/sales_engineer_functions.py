from apps.demo_data.models import TestSalesEngineer, TestSalesEngineerGroup, TestGroup
from utils.helper import generate_public_id
from .generate_user_data import generate_unique_user_data


#creates sales engineer user faker data
def create_sales_engineer(sales_manager, organization_obj, faker):

    data = generate_unique_user_data(faker, organization_obj.name, True)

    return TestSalesEngineer.objects.create(
        public_id    = generate_public_id(TestSalesEngineer),
        first_name   = data['first_name'],
        last_name    = data['last_name'],
        email        = data['email'],
        manager      = sales_manager,
        username     = data['username'],
        organization = organization_obj,
    )

def create_sales_engineer_groups(groups, organization_obj):
    # generate groups from json and append to list to recall later


    for grp in groups:

        if TestGroup.objects.filter( name = grp['name']).exists():
            continue


        TestGroup.objects.create(
            public_id    = generate_public_id(TestGroup),
            name         = grp["name"],
            description  = grp["description"],
            organization = organization_obj,
        )


    return TestGroup.objects.filter(organization = organization_obj)




#create a list of sales engineers, checks the sales engineer manager has no more than 6 sales engineers
def create_sales_engineers(sales_manager, organization_obj, faker):

    sales_engineers = list(TestSalesEngineer.objects.filter(manager = sales_manager))

    # if sales manager has count greater than 5 return sales engineer list
    if len(sales_engineers) > 5:
        return sales_engineers

    #check the remaining sales engineer needed
    remaining_engineer_count = 6 - len(sales_engineers)

    #create remaining sales engineer
    for _ in range(remaining_engineer_count):

        #create new sales engineer
        new_sales_engineer = create_sales_engineer(sales_manager, organization_obj, faker)

        #append new sales engineer to list
        sales_engineers.append(new_sales_engineer)

    return sales_engineers


#group sales engineers to sales engineer groups and checks for duplicate
def sales_engineers_group(sales_engineers, group):

    for sales_engineer in sales_engineers:
        exists = TestSalesEngineerGroup.objects.filter(sales_engineer = sales_engineer, group = group).exists()

        if exists:
            continue

        TestSalesEngineerGroup.objects.create(
            sales_engineer = sales_engineer,
            group          = group,
        )



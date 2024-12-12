from apps.demo_data.models import TestSalesRepresentative
from apps.authentication.management.commands.generated_data.generate_user_data import generate_unique_user_data, data_exists
from utils.helper import generate_public_id



#create sales rep
def create_sales_representative(sales_engineer, role, organization_obj, faker):

    while True:

        data = generate_unique_user_data(faker, organization_obj.name, False)

        if not data_exists(data, has_username = False):

            return TestSalesRepresentative.objects.create(
                public_id      = generate_public_id(TestSalesRepresentative),
                first_name     = data['first_name'],
                last_name      = data['last_name'],
                email          = data['email'],
                organization   = organization_obj,
                role           = role,
                sales_engineer = sales_engineer,
            )

#create sales rep list, each role will have no more than two reps
def create_sales_representatives(sales_engineer, role, organization_obj, faker):

    #get sales reps based on sales engineers and role
    sales_reps_list = list(TestSalesRepresentative.objects.filter(sales_engineer = sales_engineer, role = role))

    #if sales reps has 2 or more reps
    if len(sales_reps_list) > 1:

        return sales_reps_list

    sales_rep_count = 2 - len(sales_reps_list)


    for _ in range(sales_rep_count):

        new_sales_rep = create_sales_representative(sales_engineer, role, organization_obj, faker)

        sales_reps_list.append(new_sales_rep)


    return sales_reps_list
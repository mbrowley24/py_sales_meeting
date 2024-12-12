from .appointment_functions        import create_appointments, create_appointment_types
from apps.demo_data.models         import TestVertical
from .customer_functions           import create_customers
from faker                         import Faker
from .organization_functions       import create_organization
from .product_data                 import generate_product_data
from .sales_engineer_functions     import create_sales_engineers, sales_engineers_group,create_sales_engineer_groups
from .sales_engineer_mgr_functions import create_sales_engineer_manager, sales_engineer_managers_group
from .sales_rep_functions          import create_sales_representatives
from .sales_role_functions         import create_sales_roles
from utils.helper                  import generate_public_id
import os
import json



# generic filter for group list
def filter_group(groups, grp_name):

    return [grp for grp in groups if grp.name == grp_name][0]

#create test verticals/industries for test data
def create_verticals(organization_obj, verticals):

    for vertical in verticals:

        if TestVertical.objects.filter(
                organization_id = organization_obj,
                name            = vertical
        ).exists():
            continue

        TestVertical.objects.create(
            public_id       = generate_public_id(TestVertical),
            organization    = organization_obj,
            name            = vertical
        )

    return list(TestVertical.objects.filter(organization = organization_obj))


# main function to create test data for display on the demo side of the application
def start_data():

    #faker data generator
    faker = Faker()

    #generate file path
    file_name             = "fake_data.json"
    current_directory     = os.path.dirname(os.path.abspath(__file__))
    folder                = f"{current_directory}/{file_name}"


    #open file and load to json to create the sample data from the web application
    with open(folder, 'r') as file:
        data                          = json.load(file)

        #get or create organization
        organization_obj              = create_organization(data['organization'])

        #get or create groups and sales roles for dummy organization
        sales_engineering_groups      = create_sales_engineer_groups(data['groups'], organization_obj)
        sales_roles                   = create_sales_roles(data['sales_roles'], organization_obj)

        #get or create appointment meeting type
        appointment_types             = create_appointment_types(organization_obj, data['appointment_types'])

        #create verticals
        verticals                     = create_verticals(organization_obj, data['verticals'])

        #create products
        products                      = generate_product_data(data['products'])

        #sales engineer managers
        sales_engineer_managers       = create_sales_engineer_manager(organization_obj, faker)

        #create se sales manager group relationship
        sales_engineer_managers_group(sales_engineer_managers,
                                      filter_group(sales_engineering_groups, 'sales engineer managers')
                                      )

        #sales engineer managers
        for sales_manager in sales_engineer_managers:

            #create sales engineers
            sales_engineers           = create_sales_engineers(sales_manager, organization_obj, faker)

            #sales engineer group
            sales_engineers_group(sales_engineers,
                                  filter_group(sales_engineering_groups, 'sales engineers')
                                  )

            #loop through sales engineers, create sales reps and appointments to sales reps
            for sales_engineer in sales_engineers:

                #create sbs sales reps, customer and meetings
                sbs_sales_reps        = create_sales_representatives(sales_engineer,
                                                               filter_group(sales_roles, 'sbs'),
                                                               organization_obj,
                                                               faker)

                sbs_customers         = create_customers(faker,
                                                   sales_engineer,
                                                   sbs_sales_reps,
                                                   organization_obj,
                                                   verticals,
                                                   100
                                                   )

                create_appointments(sbs_customers, faker, appointment_types, products, 5)

                # create eae sales reps, customer and meetings
                eae_sales_reps        = create_sales_representatives(sales_engineer,
                                                              filter_group(sales_roles, 'eae'),
                                                              organization_obj,
                                                              faker)

                eae_customers         = create_customers(faker,
                                                   sales_engineer,
                                                   eae_sales_reps,
                                                   organization_obj,
                                                   verticals,
                                                   100
                                                   )
                create_appointments(eae_customers, faker, appointment_types, products, 15)

                # create eam sales reps, customer and meetings
                eam_sales_reps        = create_sales_representatives(sales_engineer,
                                                              filter_group(sales_roles, 'eam'),
                                                              organization_obj,
                                                              faker)

                eam_customers         = create_customers(faker,
                                                 sales_engineer,
                                                 eam_sales_reps,
                                                 organization_obj,
                                                 verticals,
                                                 100
                                                 )

                create_appointments(eam_customers, faker, appointment_types, products, 10)
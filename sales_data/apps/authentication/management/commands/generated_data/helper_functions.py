from apps.demo_data.models         import TestVertical
from .customer_functions           import create_customers
from faker                         import Faker
from io                        import TextIOBase
from .sales_engineer_functions import create_sales_engineers
from typing                    import Any

from utils.helper              import generate_public_id
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


def write_json(file: Any, content: dict ):
    json.dump(content, file, indent=4)

# main function to create test data for display on the demo side of the application
def start_data():

    #faker data generator
    faker                 = Faker()
    #generate file path
    file_name             = "fake_data.json"
    current_directory     = os.path.dirname(os.path.abspath(__file__))
    folder                = f"{current_directory}/{file_name}"
    json_data             = {}

    #open file and load to json to create the sample data from the web application
    with open(folder, 'r') as file:
        data                            = json.load(file)

        #get or create organization
        json_data['company']            = faker.company()

        #create products


        #sales engineer managers
        json_data['sales_engineer_mgr'] = [{ 'name' : f'{faker.first_name()} {faker.last_name()}'} for _ in range(6)]

        name_tracker                         = []
        company_name_tracker                 = []

        #sales engineer managers
        for i in range(len(json_data['sales_engineer_mgr'])):

            print(json_data['sales_engineer_mgr'][i])
            #create sales engineers
            json_data['sales_engineer_mgr'][i]['data'] = create_sales_engineers(faker,
                                                                                 name_tracker,
                                                                                 company_name_tracker)



    with open('demo_data/fake_sales.json', 'w') as json_file:
        write_json(json_file, json_data)



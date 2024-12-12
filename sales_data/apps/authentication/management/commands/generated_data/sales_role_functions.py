from apps.demo_data.models import TestSalesRole
from utils.helper import generate_public_id

#creates roles from json and check for duplicates
def create_sales_roles(roles, organization_obj):

    for role in roles:

        if TestSalesRole.objects.filter(name = role).exists():
            continue

        TestSalesRole.objects.create(
            public_id    = generate_public_id(TestSalesRole),
            name         = role['name'].lower(),
            description  = role['description'].lower(),
            organization = organization_obj,
        )


    return list(TestSalesRole.objects.filter(organization = organization_obj))
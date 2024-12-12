from apps.demo_data.models import TestOrganization
from utils.helper import generate_public_id



def create_organization(name):

    # organization container
    try:
        # check if the organization exists
        organization_obj = TestOrganization.objects.get(name = name)

        return organization_obj

    except TestOrganization.DoesNotExist:

        # create if it doesn't exist
        return TestOrganization.objects.create(
            public_id  = generate_public_id(TestOrganization),
            name       = name
        )
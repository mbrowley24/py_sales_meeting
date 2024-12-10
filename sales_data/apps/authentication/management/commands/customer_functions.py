from apps.demo_data.models import TestCustomer
from utils.helper import generate_public_id
import random



# creates customer using faker data and catch phases for notes
def create_customer(faker, sales_engineer, sales_rep, organization, vertical):

    while True:

        company = faker.company()

        customer_exists = TestCustomer.objects.filter(organization = organization, name = company).exists()

        if not customer_exists:

            notes = ''
            for _ in range(5):

                words = faker.catch_phrase()

                if len(notes) == 0:
                    notes += words
                else:
                    notes += f' {words}'

            return TestCustomer.objects.create(
                public_id      = generate_public_id(TestCustomer),
                organization   = organization,
                name           = company,
                notes          = notes,
                sales_rep      = sales_rep,
                sales_engineer = sales_engineer,
                vertical       = vertical
            )


# create multiple customers and return a list of customers with a default value of 100 customers
# takes in a list of customers, loops through and creates the customer_count # of customers
def create_customers(faker, sales_engineer, sales_reps, organization, verticals, customer_count = 100):

    customer_list = []

    for sales_rep in sales_reps:

        customers = list(TestCustomer.objects.filter(sales_rep = sales_rep))

        if len(customers) >= customer_count:

            customer_list.extend(customers)

            return customer_list

        remaining_customer_count = customer_count - len(customers)

        for _ in range(remaining_customer_count):

            random_vertical  = random.choice(verticals)

            new_customer     = create_customer(faker, sales_engineer, sales_rep, organization, random_vertical)

            customers.append(new_customer)

        customer_list.extend(customers)

    return customer_list
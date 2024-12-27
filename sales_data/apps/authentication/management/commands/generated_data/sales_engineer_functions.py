from .sales_rep_functions import create_sales_representatives



#creates sales engineer user faker data
def create_sales_engineer(faker, name_tracker, company_tracker):

    sales_engineer     = ""

    while True:

        sales_engineer = f'{faker.first_name()} {faker.last_name()}'

        if sales_engineer not in name_tracker:
            break



    return { 'name' : sales_engineer,
             'data' : create_sales_representatives(faker)
          }









#create a list of sales engineers, checks the sales engineer manager has no more than 6 sales engineers
def create_sales_engineers(faker, name_tracker, company_tracker):

    sales_engineers = []

    for _ in range(6):

        sales_engineer = create_sales_engineer(faker, name_tracker, company_tracker)
        sales_engineers.append(sales_engineer)


    return sales_engineers



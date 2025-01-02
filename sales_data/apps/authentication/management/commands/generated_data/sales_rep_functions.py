import random

from .appointment_functions import create_appointments


def create_performance(role):

    multiplier = [0, 1, 2, 3, 4]
    quota = 240000

    if role == 'eae':

        quota = 420000

    elif role == 'eam':

        quota = 175000

    def create_values():

        multiply = random.choices(multiplier, weights = [2, 7, 3, 2, 1], k = 1)

        return quota * multiply[0]

    performance = {
        2021 : [create_values() for _ in range(12)],
        2022 : [create_values() for _ in range(12)],
        2023 : [create_values() for _ in range(12)],
        2024 : [create_values() for _ in range(12)],
    }




    return performance



#create sales rep
def create_sales_representative(role, faker):
    data = {}

    #small business
    if role == 'sbs':

        appointments = create_appointments(faker, role)

        data = {
                'name'         : f'{faker.first_name()} {faker.last_name()}',
                'role'         : role,
                'quota'        : 2400,
                'appointments' : appointments,
                'performance'  : create_performance(role)

            }

    #account manager
    elif role == 'eam':

        data = {
                'name'         : f'{faker.first_name()} {faker.last_name()}',
                'role'         : role,
                'quota'        : 1700,
                'appointments' : create_appointments(faker, role),
                'performance'  : create_performance(role)
        }


    #enterprise account exec
    elif role == 'eae':

        data = {
                'name'         :f'{faker.first_name()} {faker.last_name()}',
                'role'         : role,
                'quota'        : 4200,
                'appointments' : create_appointments(faker, role),
                'performance'  : create_performance(role)
        }

    return data


#create sales rep list, each role will have no more than two reps
def create_sales_representatives(faker):

    roles = ['sbs', 'eam', 'eae', 'sbs', 'eam', 'eae']

    sales_reps = []

    for role in roles:

        sales_rep = create_sales_representative(role, faker)

        sales_reps.append(sales_rep)



    return sales_reps
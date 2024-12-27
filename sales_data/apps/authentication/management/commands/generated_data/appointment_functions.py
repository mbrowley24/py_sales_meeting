from apps.demo_data.models import TestAppointment, TestAppointmentType, TestAppointmentProduct
from datetime import datetime, timedelta
from django.utils import timezone
from utils.helper import generate_public_id

import random

#create random date and time between monday - friday 8am - 9pm
def random_times(faker, role):

    dates       = []
    date_count = 0

    if role == 'sbs':
        date_count = random.randint(1, 2)

    else:
        date_count = random.randint(1, 10)


    #days allow
    #allowed_days   = [0, 1, 2, 3, 4]  # Monday, Tuesday, Wednesday, Thursday, Friday

    #months
    months         = {
                      1  : 31,
                      2  : 28,
                      3  : 31,
                      4  : 30,
                      5  : 31,
                      6  : 30,
                      7  : 31,
                      8  : 31,
                      9  : 30,
                      10 : 31,
                      11 : 30,
                      12 : 31
                      } #Jan - Dec

    #set years
    years          = [2021, 2022, 2023, 2024]

    hours          = [x for x in range(8, 17)]
    minutes        = [x for x in range(0, 60)]

    #set start and end date variables
    start_time     = (8, 0)  # 8:00 AM
    end_time       = (17, 0)  # 5:00 PM

    selected_year   = random.choice(years)

    i = 0
    while i < date_count:


        month  = random.randint(1, 12)
        day    = random.randint(1, months[month])
        hour   = random.choice(hours)
        minute = random.choice(minutes)

        date = datetime(selected_year, month, day, hour, minute)

        #check if date is duplicate and if date is a week day. If date is a duplicate of date is
        #not a weekday do not increment i and do not append date
        if date not in dates:

            if date.weekday() < 5:

                dates.append(date.strftime("%Y-%m-%d %H:%M:%S"))
                i += 1


    return dates




#creates and returns appointment using faker to use catch phases in the notes sections. Current value for notes
#is 5 catch phases
def create_appointment(customer, date, faker, type_meeting, products):

    notes = ''

    #5 catches phases for notes
    for _ in range(5):

        words = faker.catch_phrase()

        #first note is not buffered by a space. All following additions will be padded with space
        if len(notes) == 0:
            notes = words

        else:

            notes = f' {words}'

    return {
        'customer' : customer,
        'date'     : date,
        'notes'    : notes,
        'products' : products,
        'type'     : type_meeting,
        'title'    : faker.bs().lower(),
    }

    #create appointment using random date. check for duplicate dates

def meeting_type(date_list, index):

    meeting = 'iah'

    if index == (len(date_list) - 1):

        meeting = 'pa'

    else:
        meeting = 'fa'


    return meeting

# create multiple appointments with the default set to 100 max appointments. The meeting_count_max
# is the upper bound for a random number of meetings starting from 1. Function will also ensure
# every customer has at least 1 meeting (iah). customers will only have on run of meetings ensuring
# meetings will not be added when initialize data functions run more one time
def create_appointments(faker, role):

    ent_products =[
        "UCaaS",
        "VoIP",
        "DRaaS",
        "BaaS",
        "Dedicated Internet",
        "Cloud Connectivity",
        "WAN Management",
        "MDR",
        "EDR",
        "Cloud Hosting",
        "Metro Ethernet",
        "Professional Services",
        "Incident Response",
        "Penetration Testing",
        "Managed Wi-Fi",
        "SD-WAN",
        "SOCaaS",
        "DDoS Protection"
    ]

    sbs_products = [
        "VoIP",
        "Dedicated Internet",
        "EDR",
        "Managed Wi-Fi",
        "SD-WAN"
    ]

    customers     = []

    if role == 'sbs':
        customers = [faker.company() for i in range(100)]
    else:
        customers = [faker.company() for i in range(50)]

    appointments  = []



    for customer in customers:

        products = []

        if role == 'sbs':
            items    = random.randint(1, 3)
            weights  = [ random.randint(1, 3) for _ in range(len(sbs_products))]
            products = random.sample(sbs_products, k = items)

        else:

            items    = random.randint(1, 5)
            weights  = [random.randint(1, 10) for _ in range(len(ent_products))]
            products = random.sample(ent_products, k = items)


        random_dates = random_times(faker, role)

        for i in range(len(random_dates)):

            type_meeting = meeting_type(random_dates, i)

            appointment  = create_appointment(customer, random_dates[i], faker, type_meeting, products)

            appointments.append(appointment)

    return appointments




def product_list(products):

    product_count = random.randint(1, 3)

    track_idx = []
    prod_list = []

    i         = 0

    while i < product_count:

        prod_idx = random.randint(0, len(products) - 1)

        if prod_idx not in track_idx:

            track_idx.append(prod_idx)

            prod_list.append(products[prod_idx])

            i += 1



    return prod_list


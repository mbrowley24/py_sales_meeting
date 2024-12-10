from apps.demo_data.models import TestAppointment, TestAppointmentType
from utils.helper import generate_public_id

import random

#create random date and time between monday - friday 8am - 9pm
def random_time(faker):


    #days allow in timezone
    allowed_days = [0, 1, 2, 3, 4]  # Monday, Tuesday, Wednesday, Thursday, Friday

    #set start and end date variables
    start_time   = (8, 0)  # 8:00 AM
    end_time     = (17, 0)  # 5:00 PM

    #generate date and time
    while True:

        #dates between the current time and three years in the past
        random_date_time = faker.date_time_between(start_date='-3y', end_date='now')

        if random_date_time.weekday() in allowed_days:

            if start_time <= (random_date_time.hour, random_date_time.minute) <= end_time:

                return random_date_time


#creates and returns appointment using faker to use catch phases in the notes sections. Current value for notes
#is 5 catch phases
def create_appointment(appointment_type, customer, faker):

    notes = ''

    #5 catches phases for notes
    for _ in range(5):

        words = faker.catch_phrase()

        #first note is not buffered by a space. All following additions will be padded with space
        if len(notes) == 0:
            notes = words

        else:

            notes = f' {words}'

    #create appointment using random date. check for duplicate dates
    while True:

        random_date = random_time(faker)

        if TestAppointment.objects.filter(customer = customer, date = random_date ).exists():
            continue


        return TestAppointment.objects.create(
            public_id      = generate_public_id(TestAppointment),
            customer       = customer,
            date           = random_time(faker),
            notes          = notes,
            organization   = customer.organization,
            sales_engineer = customer.sales_engineer,
            sales_rep      = customer.sales_rep,
            title          = faker.bs().lower(),
            type           = appointment_type,
        )

# create multiple appointments with the default set to 100 max appointments. The meeting_count_max
# is the upper bound for a random number of meetings starting from 1. Function will also ensure
# every customer has at least 1 meeting (iah). customers will only have on run of meetings ensuring
# meetings will not be added when initialize data functions run more that one time
def create_appointments(customers, faker, appointment_types, meeting_count_max = 100):

    iah                = [x for x in appointment_types if x.name == 'iah'][0]
    other_meeting_type = [x for x in appointment_types if x.name != 'iah']


    for customer in customers:

        has_iah       = TestAppointment.objects.filter(customer = customer, type = iah).exists()
        appointments  = list(TestAppointment.objects.filter(customer = customer))



        meeting_count = random.randint(1, (meeting_count_max + 1))

        if len(appointments) >= meeting_count or len(appointments) > 0:
            continue

        remaining_appointments = meeting_count - len(appointments)

        for _ in range(remaining_appointments):

            if has_iah:

                idx = random.randint(0, len(other_meeting_type) -1)

                create_appointment(other_meeting_type[idx], customer, faker)


            else:

                create_appointment(iah, customer, faker)

                has_iah = True




#create test data meeting type completely separate from production data
def create_appointment_types(organization_obj, appointment_types):

    for apt_type in appointment_types:

        if TestAppointmentType.objects.filter(name = apt_type).exists():
            continue

        TestAppointmentType.objects.create(
            public_id    = generate_public_id(TestAppointmentType),
            name         = apt_type['name'],
            description  = apt_type['description'],
            organization = organization_obj,
        )

    return list(TestAppointmentType.objects.filter(organization = organization_obj))



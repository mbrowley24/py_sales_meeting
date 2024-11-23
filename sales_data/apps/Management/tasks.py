import os
import sendgrid

from celery import shared_task
from dataclasses import dataclass
from sendgrid.helpers.mail import Mail

@dataclass
class EmailDataUserName:
    sender     : str
    name       : str
    username   : str
    recipient  : str

@dataclass
class EmailDataPassword:
    sender    : str
    name      : str
    password  : str
    recipient : str





@shared_task
def send_username_new (data):

    sg                          = sendgrid.SendGridAPIClient(api_key=os.environ.get('SEND_GRID_API_KEY'))

    email                       = Mail(
                     from_email = data.sender,
                     to_emails  = data.recipient,
                    )

    email.template              = os.environ.get('USER_NAME_TEMPLATE')

    email.dynamic_template_data = {
            'name'     : data.name,
            'username' : data.username,
    }

    #ToDo when ready to implement implement S# bucket for log files
    try:

        response                = sg.send(email)

        print(response.status_code)


    except Exception as e:

        print(e)

@shared_task
def send_password_new (data):

    sg                          = sendgrid.SendGridAPIClient(api_key=os.environ.get('SEND_GRID_API_KEY'))

    email                       = Mail(
                     from_email = data.sender,
                     to_emails  = data.recipient,
                    )

    email.template              = os.environ.get('NEW_PASSWORD_EMAIL_TEMPLATE')

    email.dynamic_template_data = {
            'name'     : data.name,
            'password' : data.password,
    }

    #ToDo when ready to implement implement S# bucket for log files
    try:

        response                = sg.send(email)

        print(response.status_code)


    except Exception as e:

        print(e)
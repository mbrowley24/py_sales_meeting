import random
import string
import re


# Check if a string is a valid email address
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


# Check if a string is a valid phone number
def is_valid_phone(phone):
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    return re.match(pattern, phone) is not None


def is_valid_numeric(value):
    return value.isnumeric()


def is_valid_monetary_value(value):
    cleaned_value = value.replace(",", "")

    pattern = r"^([0-9]{1,12})\.[0-9]{2}$"

    return re.match(pattern, cleaned_value) is not None


# Generate a random string of a given length
def generate_random_string(length=30):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# Generate a unique publicId for an entity
def generate_public_id(entity_object):
    public_id = generate_random_string(30)

    while entity_object.objects.filter(public_id=public_id).exists():
        public_id = generate_random_string(30)

    return generate_random_string(30)
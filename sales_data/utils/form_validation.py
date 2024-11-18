import re



def email_regex(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return bool(re.fullmatch(pattern, email))


def name_regex(name):
    pattern =r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-' ][A-Za-zÀ-ÖØ-öø-ÿ]+)?$"
    return bool(re.fullmatch(pattern, name))

def value_cleaner(value):

    return re.sub(r"[^\d\s]", "", value.lower())

def username_regex(username):
    pattern = r"^[a-zA-Z0-9._-]{3,50}$"
    return bool(re.fullmatch(pattern, username))



def text_regex(text):
    pattern = r"^[a-zA-Z0-9\s.,!?\"'(){}\[\]@#%^&*\-_=+:;~]*$"
    return bool(re.fullmatch(pattern, text))

def time_pattern(time):
    pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    return bool(re.fullmatch(pattern, time))


def date_pattern(date):
    pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    return bool(re.fullmatch(pattern, date))
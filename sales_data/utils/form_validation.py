import re


def email_regex(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return bool(re.fullmatch(pattern, email))


def name_regex(name):
    pattern =r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-' ][A-Za-zÀ-ÖØ-öø-ÿ]+)?$"
    return bool(re.fullmatch(pattern, name))


def username_regex(username):
    pattern = r"^[a-zA-Z0-9._-]{3,50}$"
    return bool(re.fullmatch(pattern, username))
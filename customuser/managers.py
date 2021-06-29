import re


def check_validation(password):
    p = re.compile('[1-9]')
    if not len(password) >= 8:
        return False
    if not p.findall(password):
        return False
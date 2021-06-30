import re
import random



def check_validation(password):
    p = re.compile('[1-9]')
    match = re.search(p, password)
    if len(password) >= 8 and match:
        return True
    else:
        return False


def Otp_authentication():
    otp = random.randint(1000, 9999)
    return str(otp)





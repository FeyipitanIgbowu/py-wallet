import random
import string


def generate_account_number():
    return "44" +  str(random.randrange(00000000, 99999999))

def generate_wallet_number():
    return "11" + str(random.randrange(00000000, 99999999))

def generate_reference_number():
    return "Qpw" + str(random.shuffle[string.ascii_lowercase + string.digits])

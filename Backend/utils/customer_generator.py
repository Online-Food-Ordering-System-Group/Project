import random
import string
def customer_name_generator():
    name = ''.join(random.choice(string.ascii_letters) for _ in range(7))
    return name
def phone_generator():
    phone = ''.join(random.choice(string.digits) for _ in range(10))
    return phone
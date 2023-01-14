import random
import string
def restaurant_name_generator():
    name = ''.join(random.choice(string.ascii_letters) for _ in range(5))
    return name
def restaurant_type_generator():
    data = ['Chinese','American','Japanese']
    type = data[random.randrange(3)]
    return type
def restaurant_rd_img():
    url = "https://picsum.photos/id/"+ str(random.randrange(1001)) +"200"
    return url

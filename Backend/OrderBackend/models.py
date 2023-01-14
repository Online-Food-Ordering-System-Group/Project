from datetime import datetime
from mongoengine import ( Document, StringField, ObjectIdField, DateField, IntField)

# Entity Sets
class Customer(Document):
    customerName = StringField(required=True)
    phone = StringField(required=True)

class Boss(Document):
    bossName = StringField(required = True)

class Restaurant(Document):
    restaurantName = StringField(required = True)
    restaurantType = StringField(required = True)
    restaurantURL = StringField(required = True)

class Meal(Document):
    mealName = StringField(required = True)
    imgURL = StringField(required = True)
    price = IntField(required = True)

class Order(Document):
    totalSum = IntField(required = True)
    count = IntField(required = True)
    orderDate = DateField(default=datetime.date(datetime.now()))


# Relationship Sets
class Reciept(Document):
    restaurantID = ObjectIdField(required=True)
    customerID = ObjectIdField(required=True)
    orderID = ObjectIdField(required=True)
    mealID = ObjectIdField(required=True)

class Owner(Document):
    bossID = ObjectIdField(required=True)
    restaurantID = ObjectIdField(required=True)

class Dish(Document):
    restaurantID = ObjectIdField(required=True)
    mealID = ObjectIdField(required=True)

class Money (Document):
    bossID = ObjectIdField(required=True)
    restaurantID = ObjectIdField(required= True)
    orderID = ObjectIdField(required=True)


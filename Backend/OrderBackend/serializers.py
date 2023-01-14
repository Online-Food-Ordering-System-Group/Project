from rest_framework_mongoengine.serializers import DocumentSerializer
from OrderBackend.models import *
class CustomerSerializer(DocumentSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
class BossSerializer(DocumentSerializer):
    class Meta:
        model = Boss
        fields = '__all__'
class DishSerializer(DocumentSerializer):
    class Meta:
        model = Dish
        fields = '__all__'
class MealSerializer(DocumentSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
class RestaurantSerializer(DocumentSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
class MoneySerializer(DocumentSerializer):
    class Meta:
        model = Money
        fields = '__all__'
class OrderSerializer(DocumentSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class OwnerSerializer(DocumentSerializer):
    class Meta:
        model = Owner
        fields = '__all__'
class RecieptSerializer(DocumentSerializer):
    class Meta:
        model = Reciept
        fields = '__all__'
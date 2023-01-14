from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from OrderBackend import serializers
from utils import restaurant_generator,customer_generator


@api_view(['POST'])
def create_random_boss(request):
    stringNumber = JSONParser().parse(request)
    number = eval(stringNumber['number'])
    for i in range(number):
        boss = {
            "bossName":customer_generator.customer_name_generator()#因為跟顧客名字沒有差別所以直接用這個func
        }
        boss_serializers = serializers.BossSerializer(data=boss)
        if boss_serializers.is_valid():
            boss_serializers.save()
        bossID = boss_serializers.data.get('id')
        restaurant_name = restaurant_generator.restaurant_name_generator()
        restaurant_type = restaurant_generator.restaurant_type_generator()
        restaurantURL = restaurant_generator.restaurant_rd_img()
        restaurant = {
            'restaurantName':restaurant_name,
            'restaurantType':restaurant_type,
            "restaurantURL":restaurantURL
        }
        restaurant_serializer = serializers.RestaurantSerializer(data = restaurant)
        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
        restaurantID = restaurant_serializer.data.get('id')

        owner = {
            "bossID":bossID,
            "restaurantID":restaurantID
        }
        owner_serializers = serializers.OwnerSerializer(data=owner)
        if owner_serializers.is_valid():
            owner_serializers.save()
    return JsonResponse({'message':'create'},status=status.HTTP_201_CREATED)
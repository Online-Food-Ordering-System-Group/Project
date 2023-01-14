#create restaurant 的時候要帶 boss id


from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from OrderBackend import models, serializers
from utils import meal_generator,restaurant_generator,customer_generator
import random
#測試
# data set, restaurant_number指定餐廳數量, mael_number指定每間餐廳餐點數量 
@api_view(['POST'])
def create_random_restaurant(request):
    body = JSONParser().parse(request)
    meal_number = eval(body['meal_number'])
    restaurant_number = eval(body['restaurant_number'])
    for _ in range(restaurant_number):
        restaurant_name = restaurant_generator.restaurant_name_generator()
        restaurant_type = restaurant_generator.restaurant_type_generator()
        restaurantURL = restaurant_generator.restaurant_rd_img()
        restaurant = {
            'restaurantName':restaurant_name,
            'restaurantType':restaurant_type,
            'restaurantURL':restaurantURL
        }
        restaurant_serializer = serializers.RestaurantSerializer(data = restaurant)
        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
        restaurantID = restaurant_serializer.data.get('id')
        boss = {
            "bossName":customer_generator.customer_name_generator()#因為跟顧客名字沒有差別所以直接用這個func
        }
        boss_serializers = serializers.BossSerializer(data=boss)
        if boss_serializers.is_valid():
            boss_serializers.save()
        bossID = boss_serializers.data.get('id')
        owner = {
            "bossID":bossID,
            "restaurantID":restaurantID
        }
        owner_serializers = serializers.OwnerSerializer(data=owner)
        if owner_serializers.is_valid():
            owner_serializers.save()
        #新增 meal
        for _ in range(meal_number):
            meal_name = meal_generator.food_catcher()
            price = random.randrange(501)
            imgURL = meal_generator.rd_img()
            meal = {
                'mealName': meal_name,
                'price': price,
                'imgURL':imgURL 
            }      
            meal_serializer = serializers.MealSerializer(data = meal)
            if meal_serializer.is_valid():
                meal_serializer.save()
            mealID = meal_serializer.data.get('id')
            dish = {
                'restaurantID':restaurantID,
                'mealID':mealID
            }
            dish_serializer = serializers.DishSerializer(data = dish)
            if dish_serializer.is_valid():
                dish_serializer.save()
    #response可能需要更動
    return JsonResponse({'message':'create'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_all_restaurant(request):
    restaurant_type = request.GET.get('type')
    all = request.GET.get('all')
    type_restaurant = models.Restaurant.objects.filter(restaurantType = restaurant_type)
    type_restaurant_list = list(type_restaurant)
    if all == 'false':
        print("false")
        type_restaurant_list_s = serializers.RestaurantSerializer(type_restaurant_list[0:5], many=True)
        res = JsonResponse(type_restaurant_list_s.data,status = status.HTTP_200_OK,safe = False)
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res
    else:
        type_restaurant_list_s = serializers.RestaurantSerializer(type_restaurant_list, many=True)
        res = JsonResponse(type_restaurant_list_s.data,status = status.HTTP_200_OK,safe = False)
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res
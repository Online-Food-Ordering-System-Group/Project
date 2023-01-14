from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from OrderBackend import models, serializers
from utils import meal_generator, popularity_generator
import random

@api_view(["POST"])
def create_meal(request):
    body = JSONParser().parse(request)
    meal = {
            'mealName': body['mealName'],
            'price': body['price'],
            'imgURL':body['imgURL'] 
        }
    meal_serializer = serializers.MealSerializer(data = meal)
    if meal_serializer.is_valid():
        meal_serializer.save()
    restaurantID = body['restaurantID']
    mealID = meal_serializer.data.get('id')
    dish = {
            'restaurantID':restaurantID,
            'mealID':mealID
        }
    dish_serializer = serializers.DishSerializer(data = dish)
    if dish_serializer.is_valid():
        dish_serializer.save()
    data = {
            'restaurantID':restaurantID,
            'mealID':mealID,
            'mealName': meal_serializer.data.get('mealName'),
            'price': meal_serializer.data.get('price'),
            'imgURL': meal_serializer.data.get('imgURL')
        }
    return JsonResponse(data,json_dumps_params={'ensure_ascii':False},status=status.HTTP_201_CREATED)

# data set 給定一個餐廳, 隨機產生 meal
@api_view(['POST'])
def create_random_meal(request):
    body = JSONParser().parse(request)
    number = eval(body['number'])
    for _ in range(number):
        #新增 meal
        name = meal_generator.food_catcher()
        price = random.randrange(501)
        imgURL = meal_generator.rd_img()
        meal = {
            'mealName': name,
            'price': price,
            'imgURL':imgURL 
        }      
        meal_serializer = serializers.MealSerializer(data = meal)
        if meal_serializer.is_valid():
            meal_serializer.save()
        restaurantID = body['restaurantID']
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

@api_view(["GET"])
def get_meal(request,restaurant_id):
    dish_list = list(models.Dish.objects.filter(restaurantID = restaurant_id))
    meal_list = []
    for i in range(len(dish_list)):
        meal_serializer = dict(serializers.MealSerializer(models.Meal.objects.get(id = dish_list[i].mealID)).data)
        meal_serializer['restName'] = models.Restaurant.objects.get(id = restaurant_id).restaurantName
        meal_list.append(meal_serializer)
    res = JsonResponse(meal_list,status=status.HTTP_200_OK,safe=False)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@api_view(["GET"])
def get_popularity(request):
    result = popularity_generator.result
    res = JsonResponse(result,status=status.HTTP_200_OK,safe = False)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@api_view(['GET'])
def popularity(request):
    all_meal_list = list(models.Meal.objects.all())
    meal_count = {}
    final_rank = []
    for i in range(len(all_meal_list)):
        count = models.Reciept.objects.filter(mealID = all_meal_list[i].id).count()
        meal_count[str(all_meal_list[i].id)] = count
    result = sorted(meal_count.items(),key = lambda meal_count:meal_count[1],reverse=True)
    rank_count = 1
    number_prv = result[0][1]
    
    for i in range(len(result)):
        number_now = result[i][1]
        if number_now == number_prv :
            rank = rank_count
        else :
            rank = rank_count + 1
            rank_count = rank_count + 1
            number_prv = number_now

        meal_id = result[i][0]
        try:
            meal_dict = {
                "mealName" : models.Meal.objects.get(id = meal_id).mealName,
                "shop" : models.Restaurant.objects.get(id = models.Dish.objects.get(mealID = meal_id).restaurantID).restaurantName,
                "rank" : rank,
                "click" : number_now
            }
            final_rank.append(meal_dict)
        except:
            print("dish not found : ",meal_id)
    popularity_generator.result = final_rank
    return JsonResponse(final_rank,status=status.HTTP_200_OK,safe = False)

@api_view(['GET'])
def search(request):
    q = request.GET.get('q')
    restaurant_type = request.GET.get('type')
    sort = request.GET.get('_sort')
    money_range = request.GET.get('money_range')

    
    if restaurant_type != "":    
        restaurant = models.Restaurant.objects.filter(restaurantType = restaurant_type)
    else :
        restaurant = models.Restaurant.objects.all()

    filter_dish = models.Dish.objects.filter(restaurantID__in=list(restaurant.values_list('id')))
    all_meal = models.Meal.objects.filter(id__in=filter_dish.values_list('mealID'))

    if q !="":
        all_meal = all_meal.filter(mealName__contains = q)
    if money_range == "1":
        all_meal = all_meal.filter(price__lte = 100)
    elif money_range == "2":
        all_meal = all_meal.filter(price__lte = 250).filter(price__gt = 100)
    elif money_range == "3":
        all_meal = all_meal.filter(price__lte = 500).filter(price__gt = 250)
    
    all_meal_list =list(all_meal)
    if sort =="cost_up":
        all_meal_list = list(all_meal.order_by('price'))
    elif sort =="cost_down":
        all_meal_list = list(all_meal.order_by('-price'))
    final_mael = []
    for i in all_meal_list :
        meal = {
            "id" : str(i.id),
            "mealName" : i.mealName,
            "restName" : models.Restaurant.objects.get(id = models.Dish.objects.get(mealID = i.id).restaurantID).restaurantName,
            "price" : i.price,
            "imgURL"  : i.imgURL
        }
        final_mael.append(meal)
    res = JsonResponse(final_mael,status=status.HTTP_200_OK,safe = False)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res
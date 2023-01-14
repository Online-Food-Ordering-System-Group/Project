#create order 的時候要帶 customer id, meal id, restaurant id, 

from inspect import currentframe
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from utils import income_generator
from OrderBackend import models, serializers
from utils import meal_generator,restaurant_generator,customer_generator,order_generator
import random


@api_view(['POST'])
def create_random_order(request):
    body = JSONParser().parse(request)
    meal_number = eval(body['meal_number'])
    restaurant_number = eval(body['restaurant_number'])
    #新增 restaurant
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
        #新增 boss
        boss = {
            "bossName":customer_generator.customer_name_generator()#因為跟顧客名字沒有差別所以直接用這個func
        }
        boss_serializers = serializers.BossSerializer(data=boss)
        if boss_serializers.is_valid():
            boss_serializers.save()
        bossID = boss_serializers.data.get('id')
        #新增 owner
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
            #新增 random 1~2 customer 點餐
            for _ in range(random.randrange(1,3)):
                customer_name = customer_generator.customer_name_generator()
                customer_phone = customer_generator.phone_generator()
                customer = {
                    'customerName':customer_name,
                    'phone':customer_phone
                }
                customer_serializers = serializers.CustomerSerializer(data = customer)
                if customer_serializers.is_valid():
                    customer_serializers.save()
                customerID = customer_serializers.data.get('id')
                #新增 order
                count = random.randrange(1,4)
                total_sum = count * price
                order_date = order_generator.random_date()
                order = {
                    'totalSum' :total_sum,
                    'count':count,
                    'orderDate':order_date
                }
                order_serializers = serializers.OrderSerializer(data= order)
                if order_serializers.is_valid():
                    order_serializers.save()
                orderID = order_serializers.data.get('id')
                #新增 reciept
                reciept = {
                    "restaurantID":restaurantID,
                    "customerID":customerID,
                    "orderID":orderID,
                    "mealID":mealID
                }
                reciept_serializers = serializers.RecieptSerializer(data=reciept)
                if reciept_serializers.is_valid():
                    reciept_serializers.save()
                #新增 money
                money = {
                    "bossID":bossID,
                    "restaurantID":restaurantID,
                    "orderID":orderID
                }
                money_serializers = serializers.MoneySerializer(data=money)
                if money_serializers.is_valid():
                    money_serializers.save()
    #response可能需要更動
    return JsonResponse({'message':'create'},status=status.HTTP_201_CREATED)

@api_view(["GET"])
def income(request):
    result = income_generator.final_income
    res = JsonResponse(result,status=status.HTTP_200_OK,safe=False)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@api_view(['GET'])
def income_starter(request):
    income_generator.income_generator()
    return JsonResponse({},status=status.HTTP_200_OK,safe=False)

@api_view(["POST"])
def create_order(request):
    body = JSONParser().parse(request)
    customer_name = body['name']
    customer_phone = body['phone']
    meal_list = body['mealList']
    count_list = body['count']
    result = []
    for i in range(len(meal_list)):
        #try:
            dish = models.Dish.objects.get(mealID = meal_list[i])
            restaurant_id = dish.restaurantID
            customer = list(models.Customer.objects.filter(customerName = customer_name,phone = customer_phone))
            customer_id = customer[0].id
            meal = models.Meal.objects.get(id = meal_list[i])
            meal_price = meal.price
            owner = models.Owner.objects.get(restaurantID = restaurant_id)
            boss_id = owner.bossID
            order = {
                "count":count_list[i],
                "totalSum":count_list[i] * meal_price,
            }
            order_serializer = serializers.OrderSerializer(data = order)
            if order_serializer.is_valid():
                order_serializer.save()
                result.append(order_serializer.data)
            else:
                print("order error",order_serializer.data)

            order_id = order_serializer.data.get("id")

            reciept = {
                "mealID":meal_list[i],
                "restaurantID":restaurant_id,
                "orderID":order_id,
                "customerID":customer_id
            }
            reciept_serializer = serializers.RecieptSerializer(data = reciept)
            if reciept_serializer.is_valid():
                reciept_serializer.save()
            else:
                print("reciept error",reciept_serializer.data)

            money = {
                "restaurantID":restaurant_id,
                "orderID":order_id,
                "bossID":boss_id
            }
            money_serializer = serializers.MoneySerializer(data = money)
            if money_serializer.is_valid():
                money_serializer.save()
            else:
                print("money error",money_serializer.data)
        #except:
        #    print("error")
    res = JsonResponse(result,status=status.HTTP_201_CREATED,safe=False)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

@api_view(['GET'])
def get_receipt(request):
    customer_name = request.GET.get('name')
    customer_phone = request.GET.get('phone')
    customer = list(models.Customer.objects.filter(customerName = customer_name,phone = customer_phone))[0]
    reciept = list(models.Reciept.objects.filter(customerID = customer.id))
    order_dict = {}
    result = []
    for i in reciept:
        try:
            order_id = i.orderID
            order = models.Order.objects.get(id = order_id)
            order_date = order.orderDate
            order_dict[order_id] = order_date
        except:
            print("error")
    sort_list = sorted(order_dict.items(),key = lambda sort_list:sort_list[1])
    date_prev = sort_list[0][1]
    shop_list = []
    cost_list = []
    meal_list = []
    for i in range(len(sort_list)):
        date_now = sort_list[i][1]
        order_id = sort_list[i][0]
        order_totalsum = models.Order.objects.get(id = order_id).totalSum
        
        meal_id = models.Reciept.objects.get(orderID = order_id).mealID
        meal_name = models.Meal.objects.get(id = meal_id).mealName
        
        restaurant_id = models.Reciept.objects.get(orderID = order_id).restaurantID
        restaurant_name = models.Restaurant.objects.get(id = restaurant_id).restaurantName
        
        if date_now == date_prev :
            meal_list.append(meal_name)
            shop_list.append(restaurant_name)
            cost_list.append(order_totalsum)
        else:
            day_order = {
                "date":date_prev,
                "shopList":shop_list,
                "costList":cost_list,
                "mealList":meal_list
            }
            result.append(day_order)
            shop_list = [restaurant_name]
            cost_list = [order_totalsum]
            meal_list = [meal_name]
        date_prev = date_now
    day_order = {
        "date":date_now,
        "shopList":shop_list,
        "costList":cost_list,
        "mealList":meal_list
    }
    result.append(day_order)
    res = JsonResponse(result,status=status.HTTP_200_OK,safe=False)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res
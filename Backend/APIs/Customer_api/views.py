from OrderBackend import models
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from OrderBackend import serializers 
from utils import customer_generator
import random
import string

@api_view(["POST"])
def create_user(request):
    customer = JSONParser().parse(request)
    customer_serializer = serializers.CustomerSerializer(data = customer)
    try :
        customer_db = models.Customer.objects.get(customerName = customer['customerName'])
    except :
        customer_db = None
    if customer_db != None:
        return  JsonResponse({'message':'account already create'},status=status.HTTP_400_BAD_REQUEST)
    if customer_serializer.is_valid():
            customer_serializer.save()
            res = JsonResponse(customer_serializer.data,status=status.HTTP_201_CREATED)
            res.headers["Access-Control-Allow-Origin"] = "*"
            return res
    res = JsonResponse(customer_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res

# data set 隨機產生 customer
@api_view(['POST'])
def create_random_user(request):
    stringNumber = JSONParser().parse(request)
    number = eval(stringNumber['number'])
    for i in range(number):
        phone = customer_generator.phone_generator()
        customerName = customer_generator.customer_name_generator()
        customer = {
            'customerName':customerName,
            'phone':phone,
        }       
        customer_serializer = serializers.CustomerSerializer(data = customer)
        if customer_serializer.is_valid():
            customer_serializer.save()
    return JsonResponse({'message':'create'},status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_all_user(request):
    all_customer = models.Customer.objects.all()
    all_customer_serializer = serializers.CustomerSerializer(all_customer, many=True)
    return JsonResponse(all_customer_serializer.data, status=status.HTTP_200_OK, safe=False)

@api_view(["POST","GET",'DELETE'])
def id_user(request,customer_id):
    if request.method == 'GET':
        #get_one_user
        try:
            customer = models.Customer.objects.get(id = customer_id)
            customer_serializer = serializers.CustomerSerializer(customer)
            return JsonResponse(customer_serializer.data,status =status.HTTP_200_OK, safe=False )
        except:
            print('error')
            return JsonResponse({'message':'error'},status =status.HTTP_400_BAD_REQUEST )
    
    elif request.method == 'POST':
        #update_one_user
        return 
    elif request.method =='DELETE':
        #delete_user
        return
    
@api_view(["POST"])
def login(request):
    body = JSONParser().parse(request)
    user_name = body["customerName"]
    phone = body["phone"]
    customer = models.Customer.objects.get(customerName = user_name)
    customer_serializer = serializers.CustomerSerializer(customer)
    user_name_db = customer_serializer.data.get('customerName')
    user_phone_db = customer_serializer.data.get('phone')
    if user_name == user_name_db and phone == user_phone_db:
        res = JsonResponse({'message':'access'},status =status.HTTP_200_OK )
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res
    else:
        res = JsonResponse({'message':'error'},status =status.HTTP_400_BAD_REQUEST )
        res.headers["Access-Control-Allow-Origin"] = "*"
        return res
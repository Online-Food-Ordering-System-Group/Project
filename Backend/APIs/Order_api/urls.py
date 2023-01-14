from django.urls import path
from APIs.Order_api import views
urlpatterns = [
  path('create_random_order',views.create_random_order),
  path('income',views.income),
  path('',views.create_order),
  path('reciept',views.get_receipt),
  path('income_starter',views.income_starter)
]
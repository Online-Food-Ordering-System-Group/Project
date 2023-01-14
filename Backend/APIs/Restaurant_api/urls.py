from django.urls import path
from APIs.Restaurant_api import views
urlpatterns = [
  path('create_random_restaurant',views.create_random_restaurant),
  path('',views.get_all_restaurant)
]
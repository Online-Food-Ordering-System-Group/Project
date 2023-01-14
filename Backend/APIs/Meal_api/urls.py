from django.urls import path
from APIs.Meal_api import views
urlpatterns = [
  path('create_random_meal',views.create_random_meal),
  path('create',views.create_meal),
  path('restaurant/<restaurant_id>',views.get_meal),
  path('popularity',views.get_popularity),
  path('popularity_starter',views.popularity),
  path('search',views.search)
]
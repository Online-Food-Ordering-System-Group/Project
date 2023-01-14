from django.urls import include, path
urlpatterns = [
  path('customer/', include('APIs.Customer_api.urls')),
  path('boss/',include('APIs.Boss_api.urls')),
  path('restaurant/',include('APIs.Restaurant_api.urls')),
  path('meal/',include('APIs.Meal_api.urls')),
  path('order/',include('APIs.Order_api.urls')),
]
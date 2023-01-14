from django.urls import path
from APIs.Customer_api import views
urlpatterns = [
  path('create', views.create_user),
  path('',views.get_all_user),
  path('id_user/<customer_id>',views.id_user),
  path('create_random_user',views.create_random_user),
  path('login',views.login)
]
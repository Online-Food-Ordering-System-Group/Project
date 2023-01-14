from django.urls import path
from APIs.Boss_api import views
urlpatterns = [
  path('create_random_boss',views.create_random_boss)
]
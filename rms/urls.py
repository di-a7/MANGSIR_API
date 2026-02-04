from django.urls import path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', CategoryViewset, basename = 'category')
router.register('food', FoodViewset, basename = 'food')
urlpatterns = [

]+ router.urls

from django_filters import filterset
from .models import Food

class FoodFilter(filterset.FilterSet):
   class Meta:
      model = Food
      # fields = ['category']
      fields = {
         'price': ['gte', 'lte'],
         'category__name': ['iexact'],
      }
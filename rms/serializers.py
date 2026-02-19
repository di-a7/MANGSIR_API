from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = '__all__'
      # fields = ['id','name']
      # exclude = ['name']
   
   def save(self, **kwargs):
      validated_data = self.validated_data
      count = self.Meta.model.objects.filter(name = validated_data.get('name')).count()
      if count > 0:
         raise serializers.ValidationError({"detail":"The category already exists."})
      # category = Category.objects.create(name = validated_data.get('name'))
      category = self.Meta.model(**validated_data)
      category.save()
      return category


class FoodSerialzier(serializers.ModelSerializer):
   price_with_vat = serializers.SerializerMethodField()
   category_id = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all())
   category = serializers.StringRelatedField()
   # discount 10% - > serializer method field ->get_discount
   class Meta:
      model = Food
      fields = ['id','name','price','price_with_vat','category_id','category']
   
   def get_price_with_vat(self, food:Food):
      return food.price * 0.13 + food.price

class OrderItemSerialzier(serializers.ModelSerializer):
   class Meta:
      model = OrderItem
      fields = ['food']

class OrderSerializer(serializers.ModelSerializer):
   user = serializers.HiddenField(default = serializers.CurrentUserDefault())
   items = OrderItemSerialzier(many=True)
   status = serializers.CharField(read_only=True)
   payment_status = serializers.CharField(read_only=True)
   total_price = serializers.FloatField(read_only=True)
   class Meta:
      model = Order
      fields = ['user','quantity','total_price','status','payment_status','items']
   
   def create(self, validated_data):
      items = validated_data.pop('items')
      total_price = 0
      for item in items:
         food_item = item.get('food')
         total_price += (validated_data.get('quantity') * food_item.price)
      
      order = Order.objects.create(total_price = total_price, **validated_data)
      for item in items:
         OrderItem.objects.create(order = order, food = item.get('food'))
      return order

# validated_data = {
#    "quantity": 5,
#    "total_price": 500,
# }

# items = {
#       {
#       "food": 200
#       },
#    {
#       "food": 250
#       },
#    {
#       "food": 50
#       }
# }
# class CategorySerializer(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    name = serializers.CharField()
   
#    def create(self, validated_data):
#       return Category.objects.create(name = validated_data.get('name'))
   
#    def update(self, instance, validated_data):
#       instance.name = validated_data.get('name',instance.name)
#       instance.save()
#       return instance

# validated_data = {"name":"Snacks"}
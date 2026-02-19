from django.db import models
# from django.contrib.auth.models import User
from users.models import User
# Create your models here.

class Category(models.Model): 
   name = models.CharField(max_length=25)
   
   def __str__(self):
      return self.name

class Food(models.Model):
   name = models.CharField(max_length=225)
   price = models.FloatField()
   category = models.ForeignKey(Category, on_delete=models.CASCADE)
   
   def __str__(self):
      return self.name

class Table(models.Model):
   name = models.CharField(max_length=2)
   capacity = models.IntegerField()
   avaibility = models.BooleanField(default=True)
   def __str__(self):
      return self.name

class Order(models.Model):
   PENDING = 'P'
   COMPLETE = 'C'
   DELIVERED = 'D'
   STATUS_CHOICE = {
      PENDING:'Pending',
      COMPLETE:'Completed',
      DELIVERED:'Delivered'
   }
   
   PAYMENT_CHOICES = {
      PENDING : 'Pending',
      COMPLETE : 'Completed'
   }
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   quantity = models.IntegerField()
   total_price = models.FloatField(null=True, blank=True)
   status = models.CharField(max_length=1, choices=STATUS_CHOICE, default=PENDING)
   payment_status = models.CharField(max_length=100, choices=PAYMENT_CHOICES, default = PENDING)

   def __str__(self):
      return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
   order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
   food = models.ForeignKey(Food,on_delete=models.PROTECT, related_name = 'items')

# OrderItem -> Category
# food__category__name

# OrderItem -> username
# order__user__username
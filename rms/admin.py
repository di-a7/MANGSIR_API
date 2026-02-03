from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
   list_display = ('id','name',)
admin.site.register(Category, CategoryAdmin)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
   list_display = ('name','price','category')
   list_filter = ('category',)
   search_fields = ('name','category__name')
   
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
   list_display = ('name','capacity','avaibility')
   list_filter = ('avaibility','capacity')
   list_editable = ('avaibility',)

class OrderItemInline(admin.TabularInline):
   model = OrderItem
   autocomplete_fields = ('food',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display = ('user','quantity','total_price','status','payment_status')
   list_filter = ('status','payment_status')
   search_fields = ('user__username',)
   list_editable = ('status','payment_status')
   inlines = [OrderItemInline]

# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#    list_display = ['id','order','food']
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filter import FoodFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# Create your views here.
# ModelViewset

class CategoryViewset(ReadOnlyModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer
   permission_classes = [IsAuthenticatedOrReadOnly]
   
   @extend_schema(
      parameters=[
         OpenApiParameter(name='name', description='Name of the food', required=False, type=str),
      ],
      description='This is a GET food api',
   )
   def list(self, request):
      return super().list(request)
   
   @extend_schema(
      parameters=[
         OpenApiParameter(name='name', description='Filter by name', required=False, type=str),
      ],
      description='this api delete a category',
   )
   def destroy(self, request, pk=None):
      category = Category.objects.get(id = pk)
      items = OrderItem.objects.filter(food__category = category).count()
      if items > 0:
         return Response({"detail":"Data can't be deleted. Category related to the food in OrderItem"})
      category.delete()
      return Response({"detail":"Data has been deleted."}, status = status.HTTP_204_NO_CONTENT)


class FoodViewset(ReadOnlyModelViewSet):
   queryset = Food.objects.all().select_related('category')
   serializer_class = FoodSerialzier
   pagination_class = PageNumberPagination
   filter_backends = [DjangoFilterBackend, filters.SearchFilter]
   search_fields = ['name', 'category__name']
   # filterset_fields = ['name', 'category']    # Food.objects.filter(name = 'V8 pet', category__id=2)
   filterset_class = FoodFilter
   permission_classes = [IsAuthenticatedOrReadOnly]
   
   @extend_schema(
      parameters=[
         OpenApiParameter(name='description', description='Name of the food', required=False, type=str),
      ],
      description='This is a GET food api',
   )
   def list(self, request):
      # your non-standard behaviour
      return super().list(request)

class OrderViewset(ModelViewSet):
   queryset = Order.objects.prefetch_related('items').all()
   serializer_class = OrderSerializer
   pagination_class = PageNumberPagination
   filter_backends = [DjangoFilterBackend, filters.SearchFilter]
   search_filter = ['user__username']
   filterset_field = ['status','payment_status']
   permission_classes = [IsAuthenticated]






# pagination, filtering, searching

# ViewSet 
# from rest_framework import viewsets
# class CategoryList(viewsets.ViewSet):
#    def list(self, request):
#       category = Category.objects.all()
#       serializer = CategorySerializer(category, many=True)
#       return Response(serializer.data)

#    def create(self, request):
#       serializer = CategorySerializer(data = request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response({"detail": "New data created", "data": serializer.data}, status = status.HTTP_201_CREATED)

# class CategoryDetail(viewsets.ViewSet):
#    def retrieve(self, request, pk=None):
#       category = Category.objects.get(id = pk)
#       serializer = CategorySerializer(category)
#       return Response(serializer.data)
   
#    def update(self, request, pk=None):
#       category = Category.objects.get(id = pk)
#       serializer = CategorySerializer(category , data = request.data) 
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response({"detail": "Data edited", "data": serializer.data})
   
#    def destroy(self, request, pk=None):
#       category = Category.objects.get(id = pk)
#       items = OrderItem.objects.filter(food__category = category).count()
#       if items > 0:
#          return Response({"detail":"Data can't be deleted. Category related to the food in OrderItem"})
#       category.delete()
#       return Response({"detail":"Data has been deleted."}, status = status.HTTP_204_NO_CONTENT)




# Mixins, Generic APIs
# from rest_framework import mixins
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# class CategoryList(ListCreateAPIView):
#    queryset = Category.objects.all()
#    serializer_class = CategorySerializer

# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#    queryset = Category.objects.all()
#    serializer_class = CategorySerializer
   
#    def delete(self, request, id):
#       category = Category.objects.get(id = id)
#       items = OrderItem.objects.filter(food__category = category).count()
#       if items > 0:
#          return Response({"detail":"Data can't be deleted. Category related to the food in OrderItem"})
#       category.delete()
#       return Response({"detail":"Data has been deleted."}, status = status.HTTP_204_NO_CONTENT)



# APIView
# from rest_framework.views import APIView

# class CategoryList(APIView):
#    def get(self, request):
#       category = Category.objects.all()
#       serializer = CategorySerializer(category, many=True)
#       return Response(serializer.data)

#    def post(self, request):
#       serializer = CategorySerializer(data = request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response({"detail": "New data created", "data": serializer.data}, status = status.HTTP_201_CREATED)


# class CategoryDetail(APIView):
#    def get(self, request, id):
#       category = Category.objects.get(id = id)
#       serializer = CategorySerializer(category)
#       return Response(serializer.data)
   
#    def put(self, request, id):
#       category = Category.objects.get(id = id)
#       serializer = CategorySerializer(category , data = request.data) 
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response({"detail": "Data edited", "data": serializer.data})
   
#    def delete(self, request, id):
#       category = Category.objects.get(id = id)
#       items = OrderItem.objects.filter(food__category = category).count()
#       if items > 0:
#          return Response({"detail":"Data can't be deleted. Category related to the food in OrderItem"})
#       category.delete()
#       return Response({"detail":"Data has been deleted."}, status = status.HTTP_204_NO_CONTENT)






# Function based views
# @api_view(['GET','POST'])
# def category_list(request):
#    if request.method == 'GET':
#       category = Category.objects.all()
#       serializer = CategorySerializer(category, many=True)           # serialize: objects lai convert to json
#       return Response(serializer.data)
   
   
#    elif request.method == 'POST':
#       serializer = CategorySerializer(data = request.data)           # deserialize: json is converted to objects
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response({"details":"New data added."}, status = status.HTTP_201_CREATED)


# @api_view(['GET','DELETE','PUT'])
# def category_detail(request, id):
#    category = Category.objects.get(id = id)
#    if request.method == "GET":
#       serializer = CategorySerializer(category)
#       return Response(serializer.data)
   
   
#    elif request.method == "DELETE":
#       items = OrderItem.objects.filter(food__category = category).count()
#       if items > 0:
#          return Response({"detail":"Data can't be deleted. Category related to the food in OrderItem"})
#       category.delete()
#       return Response({"detail":"Data has been deleted."}, status = status.HTTP_204_NO_CONTENT)
   
   
#    elif request.method == "PUT":
#       serializer = CategorySerializer(category,data = request.data)           # deserialize: json is converted to objects
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response({"details":"Data has been updated.", "data":serializer.data}, status = status.HTTP_201_CREATED)


# table api endpoint: route-> function-> api_view -> Tableobjects -> serialize objects -> response
# table api -> CRUD operation
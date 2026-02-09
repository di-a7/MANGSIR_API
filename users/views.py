from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers, response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
# Create your views here.
class LoginAPIView(APIView):
   def post(self, request):
      username = request.data.get("username")
      password = request.data.get("password")
      if username is None or password is None:
         raise serializers.ValidationError({"details":"Both fields are required."})
      user = authenticate(username = username,password = password)      # User.objects.filter(username=username, password=password)
      if user:
         token,_ = Token.objects.get_or_create(user = user)   #(token, created) 
         return response.Response({"token":token.key,"username":username}, status=201)
      return response.Response({"detail":"User does not exists."})

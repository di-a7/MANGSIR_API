from django.urls import path
from .views import CategoryList, CategoryDetail
urlpatterns = [
   path('category/',CategoryList.as_view()),
   path('category/<id>/',CategoryDetail.as_view())
]

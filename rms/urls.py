from django.urls import path
from .views import CategoryList, CategoryDetail
urlpatterns = [
   path('category/',CategoryList.as_view({'get':'list','post':'create'})),
   path('category/<pk>/',CategoryDetail.as_view({'get':'retrieve','put':'update','delete':'destroy'}))
]

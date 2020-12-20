from rest_framework import viewsets

from .serializers import CategorySerializer 
from .models import Category
from django.http import JsonResponse
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
   

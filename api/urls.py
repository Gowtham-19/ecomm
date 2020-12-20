from django.contrib import admin
from django.urls import path,include
from .views import home
from rest_framework.authtoken import views
urlpatterns = [
   path('',home,name='home'),
   path('category/',include('api.category.urls')),
   path('product/',include('api.product.urls')),
   path('payment/',include('api.payment.urls')),
   path('user/',include('api.user.urls')),
]
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home_modulo2, name='home_modulo2'), 
]

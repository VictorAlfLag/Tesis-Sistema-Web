from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home_modulo3, name='home_modulo3'), 
]

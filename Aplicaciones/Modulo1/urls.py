from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_modulo1, name='home_modulo1'),  
]


from django.urls import path
from . import views

app_name = 'chatbot' 

urlpatterns = [
    path('api/response/', views.get_chatbot_response, name='chatbot_api_response'),
]
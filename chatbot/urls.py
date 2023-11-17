from django.urls import path
from . import views

urlpatterns = [
    path('home', views.chatbot_view, name='home'),
]

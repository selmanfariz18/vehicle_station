from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_page, name='root_page'),
    path('root', views.root_page, name='root'),
    path('home', views.chatbot_view, name='home'),
    path('submit', views.sub, name='submit'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('solution/<str:odb_code>/', views.solution, name='solution'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='home'),
    path('serve_page/<int:problem_number>/', views.serve_pdf_page, name='serve_page'),
]

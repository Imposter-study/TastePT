from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatbotAPIView.as_view(), name="chatbot"),
]

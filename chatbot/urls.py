from django.urls import path
from ninja import NinjaAPI
from .views import router, test


api = NinjaAPI()
api.add_router("", router)

urlpatterns = [
    path("chatbot/", api.urls, name="chatbot_api"),
    path("test/", test, name="chatbot_test"),
]

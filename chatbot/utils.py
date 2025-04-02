from accounts.serializers import UserSerializer
from asgiref.sync import sync_to_async

from .chatbot import VectorStoreManager


@sync_to_async
def check_authentication(request):
    return request.user.is_authenticated


@sync_to_async
def get_user_data(user):
    return UserSerializer(user).data


@sync_to_async
def add_vector_file():
    VectorStoreManager().add_file()

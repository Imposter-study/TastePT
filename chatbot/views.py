from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from .serializers import ChatbotSerializer
from .chatbot import Chatbot_Run, VectorStoreManager
from .models import Question

User = get_user_model()


class ChatbotAPIView(APIView):

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인을 해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        serializer = ChatbotSerializer(data=request.data)
        user_data = UserSerializer(user).data

        if serializer.is_valid():
            question = serializer.validated_data["question"]

            Question.objects.create(question=question, created_by=user)
            VectorStoreManager().add_file()

            chatbot = Chatbot_Run()
            response = chatbot.ask(question, str(user_data))

            return Response({"answer": response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

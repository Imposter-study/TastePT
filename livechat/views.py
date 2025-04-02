from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer

# HTML 페이지를 렌더링하는 뷰
def chat_page(request):
    return render(request, 'livechat/index.html')


def chat_room_page(request, room_id):
    return render(request, 'livechat/chat.html', {'room_id': room_id})


class ChatRoomView(APIView):
    def get(self, request):
        chatrooms = ChatRoom.objects.all()
        serializer = ChatRoomSerializer(chatrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):  # post 메서드를 클래스 안으로 이동
        serializer = ChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # 오류 메시지 출력
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ChatRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, room_id):
        messages = ChatMessage.objects.filter(room_id=room_id)
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_id):
        if request.user.is_authenticated:  # 사용자 인증 확인
            data = request.data
            data['user'] = request.user.id
            serializer = ChatMessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save(room=ChatRoom.objects.get(id=room_id), user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
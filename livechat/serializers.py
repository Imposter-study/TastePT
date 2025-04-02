from rest_framework import serializers
from .models import ChatRoom, ChatMessage

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['content', 'nickname']

    def get_nickname(self, obj):
        return obj.user.nickname  # 사용자 모델에서 닉네임 가져오기
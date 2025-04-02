from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from .models import ChatRoom, ChatMessage
from .chatbot import Chatbot_Run
from .utils import get_user_data
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print("WebSocket 연결:", self.user)

        if self.user.is_authenticated:
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

            # 채팅방 존재 여부 확인
            try:
                self.room = await sync_to_async(ChatRoom.objects.get)(id=self.room_id)
            except ObjectDoesNotExist:
                await self.close()
                return

            await self.channel_layer.group_add(
                f"chat_{self.room_id}", self.channel_name
            )
            await self.accept()

            # 이전 채팅 기록 로드
            messages = await self.get_chat_history()
            await self.send(json.dumps({"type": "chat_history", "messages": messages}))
        else:
            await self.close()

    @sync_to_async
    def get_chat_history(self):
        messages = ChatMessage.objects.filter(room_id=self.room_id).order_by(
            "created_at"
        )
        return [
            {
                "sender": (
                    "bot"
                    if msg.message_type == ChatMessage.CHATBOT_RESPONSE
                    else (
                        "system"
                        if msg.message_type == ChatMessage.SYSTEM_MESSAGE
                        else "user"
                    )
                ),
                "message": msg.message,
                "timestamp": msg.created_at.isoformat(),
                "message_type": msg.message_type,
                "parent_id": msg.parent_message_id if msg.parent_message_id else None,
            }
            for msg in messages
        ]

    @sync_to_async
    def save_user_question(self, message):
        return ChatMessage.objects.create(
            room_id=self.room_id,
            user=self.user,
            message=message,
            message_type=ChatMessage.USER_QUESTION,
        )

    @sync_to_async
    def save_bot_response(self, message, parent_question):
        return ChatMessage.objects.create(
            room_id=self.room_id,
            user=self.user,
            message=message,
            message_type=ChatMessage.CHATBOT_RESPONSE,
            parent_message=parent_question,
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()

            if not message:
                await self.send(json.dumps({"error": "메시지가 비어 있습니다."}))
                return

            if not self.user.is_authenticated:
                await self.send(json.dumps({"error": "로그인을 해주세요."}))
                return

            # 사용자 메시지 저장
            await self.save_user_question(message)

            # 사용자 정보 가져오기
            user_data = await get_user_data(self.user)
            user_data_str = await sync_to_async(str)(user_data)

            # 챗봇 응답 생성
            chatbot = Chatbot_Run()
            response = await chatbot.ask(message, user_data_str)
            response_content = await sync_to_async(str)(response.content)

            # 챗봇 응답 저장
            await self.save_bot_response(
                response_content, await self.save_user_question(message)
            )

            # 응답 전송
            await self.send(
                json.dumps(
                    {
                        "sender": "chatbot",
                        "message_type": ChatMessage.CHATBOT_RESPONSE,
                        "message": response_content,
                        "timestamp": (
                            await sync_to_async(ChatMessage.objects.latest)(
                                "created_at"
                            )
                        ).created_at.isoformat(),
                    },
                    ensure_ascii=False,
                )
            )

        except Exception as e:
            import traceback

            traceback.print_exc()
            await self.send(
                json.dumps({"sender": "system", "error": f"오류 발생: {str(e)}"})
            )

    async def disconnect(self, close_code):
        if hasattr(self, "room_id"):
            await self.channel_layer.group_discard(
                f"chat_{self.room_id}", self.channel_name
            )
        print("WebSocket 연결 종료:", close_code)

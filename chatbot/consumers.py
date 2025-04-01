from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Question
from .chatbot import Chatbot_Run
import json
import asyncio


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print("WebSocket 연결:", self.user)
        if self.user.is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()

            if not message:
                await self.send(json.dumps({"error": "메시지가 비어 있습니다."}))
                return

            # 사용자 정보 직렬화
            user_data_dict = await sync_to_async(
                lambda: {
                    "id": self.user.id,
                    "nickname": self.user.nickname,
                    "age": self.user.age,
                    "gender": self.user.gender,
                    "preferred_cuisine": list(
                        self.user.preferred_cuisine.values_list("cuisine", flat=True)
                    ),
                    "allergies": list(
                        self.user.allergies.values_list("ingredient", flat=True)
                    ),
                    "diet": self.user.diet,
                }
            )()
            user_data_str = json.dumps(user_data_dict, ensure_ascii=False)

            # 질문 저장
            await sync_to_async(Question.objects.create)(
                question=message, created_by=self.user
            )

            # 챗봇 스트리밍 실행
            chatbot = Chatbot_Run()
            response = await chatbot.ask(message, user_data_str)

            await self.send(
                json.dumps(
                    {"sender": "chatbot", "message": response.content},
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
        print(" WebSocket 연결 종료:", close_code)

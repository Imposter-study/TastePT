from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Question
from .chatbot import Chatbot_Run
from .utils import get_user_data, create_question
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print("WebSocket 연결:", self.user)
        if self.user.is_authenticated:
            # room_id를 URL 파라미터에서 가져옵니다
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
            # 채팅방 그룹에 참여
            await self.channel_layer.group_add(
                f"chat_{self.room_id}", self.channel_name
            )
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

            # 사용자가 이미 connect에서 인증되었으므로 추가 확인은 필요 없음
            if not self.user.is_authenticated:
                await self.send(json.dumps({"error": "로그인을 해주세요."}))
                return

            # 사용자 정보 가져오기
            user_data = await get_user_data(self.user)
            user_data_str = await sync_to_async(str)(user_data)

            # 질문 저장
            await create_question(message, self.user)

            # 챗봇 스트리밍 실행
            chatbot = Chatbot_Run()
            response = await chatbot.ask(message, user_data_str)
            response_content = await sync_to_async(str)(response.content)

            await self.send(
                json.dumps(
                    {"sender": "chatbot", "message": response_content},
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
        print("WebSocket 연결 종료:", close_code)

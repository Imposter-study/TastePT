from ninja import NinjaAPI, Schema
from .chatbot import Chatbot_Run, VectorStoreManager
from .models import Question
from accounts.serializers import UserSerializer
import asyncio
from asgiref.sync import sync_to_async

api = NinjaAPI()


class ChatbotRequestSchema(Schema):
    question: str


class ChatbotResponseSchema(Schema):
    answer: str


class ErrorSchema(Schema):
    detail: str


@sync_to_async
def check_authentication(request):
    return request.user.is_authenticated


@sync_to_async
def get_user_data(user):
    return UserSerializer(user).data


@sync_to_async
def create_question(question, user):
    return Question.objects.create(question=question, created_by=user)


@sync_to_async
def add_vector_file():
    VectorStoreManager().add_file()


@api.post("", response={200: ChatbotResponseSchema, 400: ErrorSchema})
async def chatbot_endpoint(request, payload: ChatbotRequestSchema):
    await asyncio.sleep(1)

    # 사용자 인증 확인 - 비동기적으로 처리
    is_authenticated = await check_authentication(request)
    if not is_authenticated:
        return 400, {"detail": "로그인을 해주세요."}

    user = request.user
    user_data = await get_user_data(user)

    question = payload.question
    await create_question(question, user)

    # 벡터 저장소에 파일 추가 - 비동기적으로 처리
    await add_vector_file()

    # 챗봇을 통해 응답 생성
    chatbot = Chatbot_Run()
    user_data_str = await sync_to_async(str)(user_data)
    response = await chatbot.ask(question, user_data_str)

    return 200, {"answer": response}

from ninja import NinjaAPI, Schema
from .chatbot import Chatbot_Run, VectorStoreManager
from .models import Question
from accounts.serializers import UserSerializer


api = NinjaAPI()


class ChatbotRequestSchema(Schema):
    question: str


class ChatbotResponseSchema(Schema):
    answer: str


class ErrorSchema(Schema):
    detail: str


@api.post("", response={200: ChatbotResponseSchema, 400: ErrorSchema})
def chatbot_endpoint(request, payload: ChatbotRequestSchema):

    # 사용자 인증 확인
    if not request.user.is_authenticated:
        return 400, {"detail": "로그인을 해주세요."}

    user = request.user
    user_data = UserSerializer(user).data

    question = payload.question
    Question.objects.create(question=question, created_by=user)

    # 벡터 저장소에 파일 추가
    VectorStoreManager().add_file()

    # 챗봇을 통해 응답 생성
    chatbot = Chatbot_Run()
    response = chatbot.ask(question, str(user_data))

    return 200, {"answer": response}

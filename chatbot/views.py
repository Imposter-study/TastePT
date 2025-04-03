from ninja import Router
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

from .utils import check_authentication, get_user_data
from .schema import (
    ChatbotRequestSchema,
    ChatbotResponseSchema,
    ErrorSchema,
    ChatRoomSchema,
)
from .models import ChatRoom
from .chatbot import Chatbot_Run


router = Router()


# 챗봇 질문방 리스트
@router.get("room/", response={200: list[ChatRoomSchema], 400: ErrorSchema})
def list_rooms(request):
    # 로그인된 사용자만 접근 가능
    if not request.user.is_authenticated:
        return 400, {"detail": "로그인을 해주세요."}
    # 로그인된 사용자가 생성한 채팅방만 조회
    return ChatRoom.objects.filter(created_by=request.user)


# 챗봇 질문방 생성
@router.post("room/", response={200: ChatRoomSchema, 400: ErrorSchema})
def create_room(request, room: ChatRoomSchema):
    # 로그인된 사용자만 접근 가능
    if not request.user.is_authenticated:
        return 400, {"detail": "로그인을 해주세요"}

    # name 필드가 제공되지 않았을 경우 오류 처리
    if not room.name:
        return 400, {"detail": "Room name을 지정해주세요."}

    # 채팅방 생성 시, 현재 로그인된 사용자(user)를 추가
    chat_room = ChatRoom.objects.create(name=room.name, created_by=request.user)
    return chat_room


# 챗봇 질문방 조회
@router.get("room/{room_id}/", response={200: ChatRoomSchema, 400: ErrorSchema})
def get_room(request, room_id: int):
    # 로그인된 사용자만 접근 가능
    if not request.user.is_authenticated:
        return 400, {"detail": "로그인을 해주세요."}
    # 해당 채팅방이 로그인된 사용자에 의해 생성된 것인지 확인
    room = get_object_or_404(ChatRoom, id=room_id, created_by=request.user)
    return room


# 챗봇 질문방 이름 수정
@router.put("room/{room_id}/", response={200: ChatRoomSchema, 400: ErrorSchema})
def update_room(request, room_id: int, room: ChatRoomSchema):
    # 로그인된 사용자만 접근 가능
    if not request.user.is_authenticated:
        return 400, {"detail": "로그인을 해주세요."}
    # 해당 채팅방이 로그인된 사용자에 의해 생성된 것인지 확인
    chat_room = get_object_or_404(ChatRoom, id=room_id, created_by=request.user)
    chat_room.name = room.name
    chat_room.save()
    return chat_room


# 챗봇 질문방 삭제
@router.delete("room/{room_id}/", response={200: dict, 400: ErrorSchema})
def delete_room(request, room_id: int):
    # 로그인된 사용자만 접근 가능
    if not request.user.is_authenticated:
        return 400, {"detail": "로그인을 해주세요."}
    # 해당 채팅방이 로그인된 사용자에 의해 생성된 것인지 확인
    chat_room = get_object_or_404(ChatRoom, id=room_id, created_by=request.user)
    chat_room.delete()
    return {"success": True}


# 챗봇 테스트용(비동기api)
@router.post("/test/", response={200: ChatbotResponseSchema, 400: ErrorSchema})
async def chatbot_endpoint(request, payload: ChatbotRequestSchema):

    # 사용자 인증 확인 - 비동기적으로 처리
    is_authenticated = await check_authentication(request)
    if not is_authenticated:
        return 400, {"detail": "로그인을 해주세요."}

    user = request.user
    user_data = await get_user_data(user)

    question = payload.question

    # 챗봇을 통해 응답 생성
    chatbot = Chatbot_Run()
    user_data_str = await sync_to_async(str)(user_data)
    response = await chatbot.ask(question, user_data_str)
    response_content = await sync_to_async(str)(response.content)

    return 200, {"answer": response_content}


from django.shortcuts import render


def test(request):
    return render(request, "chatbot/test.html")

from django.urls import path, re_path
from .views import ChatRoomView, chat_page, chat_room_page, ChatMessageView
from . import consumers  

# ✅ WebSocket URL 패턴 수정
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),  
]

urlpatterns = [
    path('chat/', chat_page, name='chat_page'),
    path('chat/<str:room_id>/', chat_room_page, name='chat_room_page'), 
    path('chatrooms/', ChatRoomView.as_view(), name='chatroom-list'),  
    path('chatrooms/<int:room_id>/', ChatRoomView.as_view(), name='chatroom-detail'),
    path('chatrooms/<int:room_id>/messages/', ChatMessageView.as_view(), name='chatmessage-list'),
]

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Recipe(models.Model):
    csv_file = models.FileField(upload_to="csv_file/")
    is_embedded = models.BooleanField(default=False)


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Created by {self.created_by.username})"


class ChatMessage(models.Model):
    # 메세지 타입 선택
    USER_QUESTION = "question"
    CHATBOT_RESPONSE = "response"
    SYSTEM_MESSAGE = "system"

    MESSAGE_TYPES = [
        (USER_QUESTION, "User Question"),
        (CHATBOT_RESPONSE, "Chatbot Response"),
        (SYSTEM_MESSAGE, "System Message"),
    ]

    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    # 메세지 타입 필드
    message_type = models.CharField(
        max_length=15, choices=MESSAGE_TYPES, default=USER_QUESTION
    )

    # 유저 질문에 대한 답변
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="responses",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        message_preview = (
            self.message[:50] + "..." if len(self.message) > 50 else self.message
        )
        return f"{self.user.username} ({self.message_type}): {message_preview}"

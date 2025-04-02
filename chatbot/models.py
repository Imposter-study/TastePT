from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Question(models.Model):
    question = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Recipe(models.Model):
    csv_file = models.FileField(upload_to="csv_file/")
    is_embedded = models.BooleanField(default=False)


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, related_name="messages", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="questioner", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content}"

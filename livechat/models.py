from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    hashtags = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 다른 모델에서 상속만 가능하도록 설정


class Post(TimeStamp):
    title = models.CharField(max_length=64)
    content = models.TextField()
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    thumbnail = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class UploadedImage(models.Model):
    image = models.URLField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image


class Comment(TimeStamp):
    content = models.TextField()
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    parent = models.ForeignKey(
        to="self", on_delete=models.CASCADE, null=True, related_name="reply_comments"
    )

    def __str__(self):
        return self.content[:10]

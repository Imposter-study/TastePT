from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 다른 모델에서 상속만 가능하도록 설정


# Create your models here.
class Post(TimeStamp):
    title = models.CharField(max_length=64)
    content = models.TextField()
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    thumbnail = models.ImageField(blank=True, upload_to="thumbnail/%Y/%m/%d")

    def __str__(self):
        return self.title


class UploadedImage(models.Model):
    image = models.ImageField(upload_to="posts/%Y/%m/%d")  # 업로드 경로 지정
    uploaded_at = models.DateTimeField(auto_now_add=True)


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

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


class Report(models.Model):
    reporter = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name="reports")
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True, related_name="reports")
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, null=True, related_name="reports")

    class Meta:
        # 중복 신고가 불가능하도록 여러 필드에 대해 unique 옵션 설정
        unique_together = ["reporter", "post", "comment"]

    def __str__(self):
        if self.post:
            return f"{self.reporter.nickname}님이 게시글 {self.post.id}번을 신고하였습니다."
        elif self.comment:
            return f"{self.reporter.nickname}님이 댓글 {self.comment.id}번을 신고하였습니다."

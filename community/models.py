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
    # image = models.ImageField(blank=True, upload_to="post/%Y/%m/%d")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title

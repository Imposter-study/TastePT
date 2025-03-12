from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, UploadedImage

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "nickname"]


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ["image"]  # 'image' 필드는 모델에서 정의된 필드

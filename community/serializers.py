from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, UploadedImage, Comment

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nickname",
            "profile_picture",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    reply_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["post", "author"]

    def get_reply_comments(self, instance):
        # 부모 댓글만 reply_comments를 포함하도록 처리
        if instance.parent is None:
            reply_comments = Comment.objects.filter(parent=instance)
            serializer = CommentSerializer(reply_comments, many=True)
            return serializer.data
        return []  # 자식 댓글은 빈 배열로 반환


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    # comments = CommentSerializer(read_only=True, many=True)
    comments = serializers.SerializerMethodField()  # 커스텀 필드로 부모 댓글만 가져오기

    class Meta:
        model = Post
        fields = "__all__"

    def get_comments(self, obj):
        # 부모 댓글만 필터링하여 반환
        comments = obj.comments.filter(parent=None)  # 부모 댓글만 가져오기
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ["image"]  # 'image' 필드는 모델에서 정의된 필드

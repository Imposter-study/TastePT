import boto3
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Prefetch
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Post, Comment, UploadedImage
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, ImageUploadSerializer, CommentSerializer
from .pagenations import PostPageNumberPagination

User = get_user_model()


# Create your views here.
# 생성, 목록조회, 상세조회, 수정, 삭제
class PostViewSet(ModelViewSet):
    queryset = Post.objects.order_by("-created_at").prefetch_related(
        Prefetch("comments", queryset=Comment.objects.order_by("-created_at"))
    )
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = PostPageNumberPagination

    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):
        """특정 게시글에 댓글 생성"""
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.save(post=post, author=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def perform_create(self, serializer):
        user = self.request.user
        # 게시글 생성 시 요청한 사용자를 게시글 작성자로 할당
        serializer.save(author=user)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )
        return queryset


class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if "image" not in request.FILES:
            return Response(
                {"error": "이미지 파일이 제공되지 않았습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        image_file = request.FILES["image"]

        ext = image_file.name.split(".")[-1] if "." in image_file.name else ""
        safe_filename = f"{uuid.uuid4().hex}.{ext}"

        now = datetime.now()
        relative_path = f"posts/{now.year}/{now.month}/{now.day}/{safe_filename}"

        # DEBUG 모드에 따라 저장 로직 분기
        if settings.DEBUG:
            # 로컬 저장소에 저장
            try:
                file_path = default_storage.save(
                    relative_path, ContentFile(image_file.read())
                )
                file_url = settings.MEDIA_URL + file_path

                serializer = ImageUploadSerializer(data={"image": file_url})
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"file_path": file_url}, status=status.HTTP_201_CREATED
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response(
                    {"error": f"이미지 업로드 실패: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            # S3에 업로드
            try:
                s3_client = boto3.client(
                    "s3",
                    region_name=settings.AWS_S3_REGION_NAME,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )

                # S3에 업로드
                s3_client.upload_fileobj(
                    image_file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    relative_path,
                    ExtraArgs={
                        "ContentType": image_file.content_type,
                        "ACL": settings.AWS_DEFAULT_ACL,
                    },
                )

                if (
                    hasattr(settings, "AWS_S3_CUSTOM_DOMAIN")
                    and settings.AWS_S3_CUSTOM_DOMAIN
                ):
                    file_url = (
                        f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{relative_path}"
                    )
                else:
                    file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{relative_path}"

                # 모델에 저장
                serializer = ImageUploadSerializer(data={"image": file_url})
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"file_path": file_url}, status=status.HTTP_201_CREATED
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response(
                    {"error": f"S3 이미지 업로드 실패: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


# 댓글 수정 & 삭제 (PUT, DELETE)
class CommentUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

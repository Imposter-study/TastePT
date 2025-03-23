import boto3
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings
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
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = request.FILES["image"]

        # 안전한 파일명으로 변환
        ext = image_file.name.split(".")[-1] if "." in image_file.name else ""
        safe_filename = f"{uuid.uuid4().hex}.{ext}"

        # S3 경로 지정 (연/월/일 구조)
        now = datetime.now()
        path = f"posts/{now.year}/{now.month}/{now.day}/{safe_filename}"

        # S3 클라이언트 생성 및 업로드
        s3_client = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
        try:
            s3_client.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                path,
                ExtraArgs={
                    "ContentType": image_file.content_type,
                    "ACL": "public-read",  # 공개 읽기 권한 설정
                }
            )

            # 파일 URL 생성
            if settings.AWS_S3_CUSTOM_DOMAIN:
                file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{path}"
            else:
                file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{path}"

            # 데이터베이스에 URL 저장
            uploaded_image = UploadedImage.objects.create(image=file_url)

            return Response(
                {"file_path": file_url},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"이미지 업로드 실패: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 댓글 수정 & 삭제 (PUT, DELETE)
class CommentUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

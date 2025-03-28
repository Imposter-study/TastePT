from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Post, Comment, Report
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, ImageUploadSerializer, CommentSerializer
from .pagenations import PostPageNumberPagination
from .utils import upload_image

User = get_user_model()


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

    def create(self, request, *args, **kwargs):
        try:
            # 썸네일 이미지 처리
            thumbnail_file = request.FILES.get("thumbnail")
            thumbnail_url = (
                upload_image(thumbnail_file, directory="thumbnail")
                if thumbnail_file
                else ""
            )

            # 데이터에 썸네일 URL 추가
            data = request.data.copy()
            if thumbnail_url:
                data["thumbnail"] = thumbnail_url

            # 시리얼라이저 처리 및 저장
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()

            # 썸네일 이미지 처리
            thumbnail_file = request.FILES.get("thumbnail")
            thumbnail_url = (
                upload_image(thumbnail_file, directory="thumbnail")
                if thumbnail_file
                else ""
            )

            # 데이터에 썸네일 URL 추가
            data = request.data.copy()
            if thumbnail_url:
                data["thumbnail"] = thumbnail_url

            # 시리얼라이저 처리 및 저장
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if "image" not in request.FILES:
            return Response(
                {"error": "이미지 파일이 제공되지 않았습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        image_file = request.FILES["image"]

        try:
            file_url = upload_image(image_file)

            # 모델에 저장
            serializer = ImageUploadSerializer(data={"image": file_url})
            if serializer.is_valid():
                serializer.save()
                return Response({"file_path": file_url}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"이미지 업로드 실패: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 댓글 수정 & 삭제 (PUT, DELETE)
class CommentUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        type = request.data["type"]
        reporter = request.user

        if type == "post":
            post = get_object_or_404(Post, pk=pk)
            comment = None
        elif type - "comment":
            post = None
            comment = get_object_or_404(Comment, pk=pk)
        report = Report.objects.filter(reporter=reporter, post=post, comment=comment)

        if report:
            return Response({"detail": "이미 신고한 게시글/댓글 입니다"}, status=400)

        Report.objects.create(reporter=reporter, post=post, comment=comment)

        return Response({"detail": "신고가 완료되었습니다."}, status=201)

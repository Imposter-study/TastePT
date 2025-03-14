from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Post, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, ImageUploadSerializer, CommentSerializer

User = get_user_model()


# Create your views here.
# 생성, 목록조회, 상세조회, 수정, 삭제
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):
        """특정 게시글에 댓글 생성"""
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user = User.objects.get(id=1)  # 프론트 테스트용 사용자 지정
            serializer.save(post=post, author=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def perform_create(self, serializer):
        user = self.request.user
        user = User.objects.get(id=1)
        # 게시글 생성 시 요청한 사용자를 게시글 작성자로 할당
        serializer.save(author=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # 삭제 후 커스텀 응답 반환
        self.perform_destroy(instance)
        return Response(
            {"detail": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )


class ImageUploadView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"file_path": serializer.data["image"]}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정 & 삭제 (PUT, DELETE)
class CommentUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        # 삭제 처리
        super().destroy(request, *args, **kwargs)
        return Response(
            {"detail": "삭제가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


# Create your views here.
# 생성, 목록조회, 상세조회, 수정, 삭제
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # 게시글 생성 시 요청한 사용자를 게시글 작성자로 할당
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # 작성자만 삭제할 수 있도록 권한 검사
        if instance.author != request.user:
            return Response(
                {"error": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(instance)

        # 삭제 후 커스텀 응답 반환
        return Response(
            {"detail": "게시글이 삭제되었습니다."}, status=status.HTTP_200_OK
        )

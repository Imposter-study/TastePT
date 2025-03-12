from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, ImageUploadSerializer

User = get_user_model()


# Create your views here.
# 생성, 목록조회, 상세조회, 수정, 삭제
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        user = User.objects.get(id=1)
        print("\n\n\n\n", user)
        # 게시글 생성 시 요청한 사용자를 게시글 작성자로 할당
        serializer.save(author=user)

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


class ImageUploadView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"file_path": serializer.data["image"]}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

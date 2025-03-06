from django.contrib.auth import authenticate, get_user_model, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignUpSerializer


User = get_user_model()


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # 사용자 인증
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"detail": "사용자 정보가 일치하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 로그인 처리 (세션에 사용자 정보 저장)
        login(request, user)

        return Response(
            {
                "detail": "로그인 성공",
                "nickname": user.nickname,  # 로그인된 사용자 이름 반환 (선택 사항)
            },
            status=status.HTTP_200_OK,
        )

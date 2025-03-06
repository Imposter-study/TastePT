from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignUpSerializer


User = get_user_model()


class UserAPIView(APIView):
    # 회원가입
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInAPIView(APIView):
    # 로그인
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"detail": "사용자 정보가 일치하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)

        return Response(
            {
                "detail": "로그인 성공",
                "nickname": user.nickname,
            },
            status=status.HTTP_200_OK,
        )


class SignOutAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "이미 로그아웃된 상태입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logout(request)

        return Response(
            {"detail": "로그아웃 성공"},
            status=status.HTTP_200_OK,
        )

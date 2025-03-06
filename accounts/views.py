from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignUpSerializer, ProfileUpdateSerializer


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

    # 개인정보 수정
    @permission_classes([IsAuthenticated])
    def put(self, request):
        user = request.user

        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원탈퇴
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user
        password = request.data.get("password")

        print(password)
        print(user.password)

        if (not user.has_usable_password()) or (user.check_password(password)):
            request.user.is_active = False
            request.user.deactivate_time = timezone.now()
            request.user.save()

            return Response(
                {"message": "회원이 비활성화 되었습니다."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"massage": "비밀번호가 일치하지 않습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, nickname):
        return get_object_or_404(User, nickname=nickname)

    # 유저 프로필 조회
    def get(self, request, nickname):

        user = self.get_object(nickname)

        return Response(
            {
                "nickname": user.nickname,
                "age": user.age,
                "gender": user.gender,
                # "allergy": 예정
                # "favorite": 예정
            },
            status=status.HTTP_200_OK,
        )


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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response(
            {"detail": "로그아웃 성공"},
            status=status.HTTP_200_OK,
        )

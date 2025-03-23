from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from dotenv import load_dotenv
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
import os
import requests

from .models import (
    Allergy,
    PreferredCuisine,
    NicknamePrefix,
    NicknameSuffix,
    EmailVerificationToken,
)
from .serializers import (
    SignUpSerializer,
    ProfileUpdateSerializer,
    PasswordSerializer,
    UserSerializer,
    AllergySerializer,
    PreferredCuisineSerializer,
)

# log
import logging

logger = logging.getLogger("accounts")

load_dotenv()
User = get_user_model()


class UserAPIView(APIView):
    # 회원가입
    @extend_schema(
        tags=["회원"],
        summary="회원가입",
        description="회원가입 API, 비회원이 회원가입을 진행합니다.",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(description="회원 가입 완료, 유저 생성"),
            400: OpenApiResponse(description="email, password 입력값이 잘못된 경우"),
        },
    )
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
        logger.debug("프로필 업데이트 시작")
        user = request.user

        # 프로필 사진 업로드 로깅
        if "profile_picture" in request.FILES:
            profile_pic = request.FILES["profile_picture"]
            logger.info(
                f"프로필 사진 정보: {profile_pic.name}, {profile_pic.size}, {profile_pic.content_type}"
            )

            # 안전한 파일명으로 변환
            import uuid

            ext = profile_pic.name.split(".")[-1] if "." in profile_pic.name else ""
            profile_pic.name = f"{uuid.uuid4().hex}.{ext}"
            logger.info(f"변환된 파일명: {profile_pic.name}")

        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                updated_user = serializer.save()
                if "profile_picture" in request.FILES and updated_user.profile_picture:
                    logger.info(
                        f"프로필 사진 저장 성공: {updated_user.profile_picture.url}"
                    )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"프로필 업데이트 오류: {str(e)}", exc_info=True)
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        logger.error(f"유효성 검증 오류: {serializer.errors}")
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
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # 비밀번호 수정
    def put(self, request):
        serializer = PasswordSerializer(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"detail": "비밀번호가 성공적으로 변경되었습니다."},
                status=status.HTTP_200_OK,
            )

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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response(
            {"detail": "로그아웃 성공"},
            status=status.HTTP_200_OK,
        )


class AllergiesListAPIView(ListAPIView):

    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer


class PreferredCuisineListAPIView(ListAPIView):

    queryset = PreferredCuisine.objects.all()
    serializer_class = PreferredCuisineSerializer


class CreateRandomNicknameAPIView(APIView):
    def get(self, request):
        prefix_query = NicknamePrefix.objects.all()
        suffix_query = NicknameSuffix.objects.all()

        prefix = prefix_query.order_by("?").first()
        suffix = suffix_query.order_by("?").first()

        nickname = f"{prefix.word} {suffix.word}"

        return Response(
            {
                "nickname": nickname,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
def check_signin_view(request):
    if request.user.is_authenticated:
        return Response(
            {
                "authenticated": True,
                "user": request.user.nickname,
                "profile_img": (
                    request.user.profile_picture.url
                    if request.user.profile_picture
                    else False
                ),
            }
        )
    return Response({"authenticated": False})


class SocialSigninView(APIView):
    def get(self, request, provider):
        if provider == "kakao":
            client_id = os.getenv("KAKAO_CLIENT_ID")
            redirect_domain = os.getenv("REDIRECT_DOMAIN")

            redirect_uri = (
                f"{redirect_domain}/api/v1/accounts/social/callback/{provider}"
            )
            auth_url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
            return Response({"auth_url": auth_url})
            # return redirect(auth_url)


class SocialCallbackView(APIView):
    def get(self, request, provider):

        code = request.GET.get("code")
        access_token = self.get_token(provider, code)
        user_info = self.get_user(provider, access_token)
        user = self.get_or_create_user(provider, user_info)
        login(request, user)

        redirect_url = os.getenv("FRONT_DOMAIN").split(",")[0]
        return redirect(redirect_url)

    def get_token(self, provider, code):
        if provider == "kakao":
            token_url = "https://kauth.kakao.com/oauth/token"
            client_id = os.getenv("KAKAO_CLIENT_ID")

        domain = os.getenv("REDIRECT_DOMAIN")

        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": f"{domain}/api/v1/accounts/social/callback/{provider}",
            "code": code,
        }

        response = requests.post(token_url, data)
        return response.json().get("access_token")

    def get_user(self, provider, access_token):
        if provider == "kakao":
            user_info_url = "https://kapi.kakao.com/v2/user/me"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        response = requests.get(user_info_url, headers=headers)
        return response.json().get("kakao_account")

    def get_or_create_user(self, provider, user_info):
        defaults = {"nickname": user_info.get("profile").get("nickname")}

        # 프로필 이미지 경로로 인해 주석처리
        # if user_info.get("profile").get("profile_image_url"):
        #     defaults["profile_picture"] = user_info.get("profile").get(
        #         "profile_image_url"
        #     )

        # 유저가 이미 있으면 유저 정보를 가져오고 없으면 유저 생성
        user, created = User.objects.get_or_create(
            email=user_info.get("email"), defaults=defaults
        )

        if created:
            user.set_unusable_password()
            user.save()

        return user


@api_view(["GET"])
def verify_email(request, token):
    token_obj = get_object_or_404(EmailVerificationToken, token=token)
    user = token_obj.user
    user.is_active = True  # 계정 활성화
    user.save()
    token_obj.delete()  # 사용된 토큰 삭제
    domain = os.getenv("FRONT_DOMAIN").split(",")[0]
    return redirect(f"{domain}/signin")

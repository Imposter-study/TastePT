import os

from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
from .tasks import send_email

from .models import EmailVerificationToken

load_dotenv()


def send_activation_email(user):
    domain = os.getenv("DOMAIN")
    token = EmailVerificationToken.objects.create(user=user)
    activation_link = f"{domain}/api/v1/accounts/verify-email/{token.token}/"

    subject = "[TastePT] 회원가입을 위한 이메일 인증을 완료해주세요."
    message = f"다음 링크를 클릭하여 이메일을 인증해주세요: \n {activation_link}"

    send_email.delay(
        subject,
        message,
        [user.email],
    )

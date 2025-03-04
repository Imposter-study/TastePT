from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# 커스텀 유효성 검사 정의
username_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9@./+\-_ ]+$",
    message=_(
        "사용자 이름에는 알파벳 대소문자, 공백 및 특수문자(@, ., /, +, -, _)만 포함 가능합니다."
    ),
)


class CustomUserManager(UserManager):
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields.setdefault("role", "A")

        return self._create_user(username, None, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ("A", "ADMIN"),
        ("S", "STAFF"),
        ("U", "USER"),
    ]

    nickname = models.CharField(max_length=20, unique=True, blank=False)
    role = models.CharField(choices=ROLE_CHOICES, max_length=1, default="U")

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],  # 커스텀 유효성 검사 사용
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    REQUIRED_FIELDS = ["nickname"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# 커스텀 유효성 검사 정의
email_validator = EmailValidator(message=_("유효한 이메일 주소를 입력하세요."))


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

    GENDER_CHOICES = [
        ("M", "남자"),
        ("F", "여자")
    ]

    # 비활성화 필드
    username = None
    first_name = None
    last_name = None

    nickname = models.CharField(max_length=20, unique=True, blank=False)
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_(
            "Required. 254 characters or fewer. Must be a valid email address."
        ),
        validators=[email_validator],
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )

    # 선택 필드
    age = models.IntegerField(blank=False, null=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=1, blank=True, null=True
    )

    # 비공개 필드
    role = models.CharField(choices=ROLE_CHOICES, max_length=1, default="U")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email

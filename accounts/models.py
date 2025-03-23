from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# 커스텀 유효성 검사 정의
email_validator = EmailValidator(message=_("유효한 이메일 주소를 입력하세요."))


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 해시화
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields.setdefault("role", "A")

        user = self.model(
            email=email, password=password, nickname="admin", **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user


class PreferredCuisine(models.Model):
    cuisine = models.CharField(max_length=10)

    def __str__(self):
        return self.cuisine


class Allergy(models.Model):
    ingredient = models.CharField(max_length=10)

    def __str__(self):
        return self.ingredient


class User(AbstractUser):
    ROLE_CHOICES = [
        ("A", "ADMIN"),
        ("S", "STAFF"),
        ("U", "USER"),
    ]

    GENDER_CHOICES = [("M", "남자"), ("F", "여자")]

    # 비활성화 필드
    username = None
    first_name = None
    last_name = None

    # 필수 필드
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
    nickname = models.CharField(max_length=30, unique=True)

    # 선택 필드
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=1, blank=True, null=True
    )
    allergies = models.ManyToManyField(Allergy, blank=True)
    preferred_cuisine = models.ManyToManyField(PreferredCuisine, blank=True)
    diet = models.BooleanField(default=False)
    profile_picture = models.URLField(null=True, blank=True)

    # 비공개 필드
    role = models.CharField(choices=ROLE_CHOICES, max_length=1, default="U")
    deactivate_time = models.DateTimeField(default=None, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class NicknamePrefix(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word


class NicknameSuffix(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

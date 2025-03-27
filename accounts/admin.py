from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.html import format_html
from accounts.models import (
    Allergy,
    PreferredCuisine,
    NicknamePrefix,
    NicknameSuffix,
)

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ("nickname", "email", "is_staff", "is_active", "last_login")
    list_filter = ("is_staff", "is_active")
    search_fields = ("nickname", "email")
    actions = ["send_email_action"]

    def send_email_action(self, request, queryset):
        """선택한 사용자에게 이메일 보내기"""
        for user in queryset:
            if user.email:
                send_mail(
                    subject="관리자 공지",
                    message="안녕하세요, 관리자에서 보내는 메일입니다.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
        self.message_user(request, "선택한 사용자에게 이메일을 전송했습니다.")

    send_email_action.short_description = "선택한 사용자에게 이메일 보내기"


class NicknamePrefixAdmin(admin.ModelAdmin):
    list_display = ("id", "word")
    search_fields = ("word",)
    ordering = ("word",)


class NicknameSuffixAdmin(admin.ModelAdmin):
    list_display = ("id", "word")
    search_fields = ("word",)
    ordering = ("word",)


admin.site.register(User, UserAdmin)
admin.site.register(Allergy)
admin.site.register(PreferredCuisine)
admin.site.register(NicknamePrefix, NicknamePrefixAdmin)
admin.site.register(NicknameSuffix, NicknameSuffixAdmin)

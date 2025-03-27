from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.timezone import now
from accounts.models import (
    Allergy,
    PreferredCuisine,
    NicknamePrefix,
    NicknameSuffix,
    EmailMessage,
)

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ("nickname", "email", "is_staff", "is_active", "last_login")
    list_filter = ("is_staff", "is_active")
    search_fields = ("nickname", "email")


class NicknamePrefixAdmin(admin.ModelAdmin):
    list_display = ("id", "word")
    search_fields = ("word",)
    ordering = ("word",)


class NicknameSuffixAdmin(admin.ModelAdmin):
    list_display = ("id", "word")
    search_fields = ("word",)
    ordering = ("word",)


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ["subject", "created_at", "sent_at"]
    filter_horizontal = ("recipients",)  # 다중선택
    actions = ["send_selected_emails"]

    def send_selected_emails(self, request, queryset):
        for email_message in queryset:
            recipient_list = [
                user.email for user in email_message.recipients.all() if user.email
            ]

            if recipient_list:
                send_mail(
                    subject=email_message.subject,
                    message=email_message.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
                email_message.sent_at = now()
                email_message.save()

        self.message_user(request, f"{queryset.count()}개의 이메일을 전송하였습니다.")

    send_selected_emails.short_description = "선색한 이메일 전송"


admin.site.register(User, UserAdmin)
admin.site.register(Allergy)
admin.site.register(PreferredCuisine)
admin.site.register(NicknamePrefix, NicknamePrefixAdmin)
admin.site.register(NicknameSuffix, NicknameSuffixAdmin)
admin.site.register(EmailMessage, EmailMessageAdmin)

from django.contrib import admin
from django.contrib.auth import get_user_model
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

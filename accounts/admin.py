from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ("nickname", "email", "is_staff", "is_active", "last_login")
    list_filter = ("is_staff", "is_active")
    search_fields = ("nickname", "email")


admin.site.register(User, UserAdmin)

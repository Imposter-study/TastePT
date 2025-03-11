from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("csv_file", "is_embedded")  # Admin 페이지에서 보이는 컬럼 설정
    readonly_fields = (
        "is_embedded",
    )  # `is_embedded`는 관리자도 수정 불가능 (읽기 전용)
    list_filter = ("is_embedded",)  # 필터 추가 (임베딩 여부별로 정렬 가능)

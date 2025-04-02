from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Only authors can be modified/deleted, and other users can only read
    """

    def has_object_permission(self, request, view, obj):
        # 조회(GET, HEAD, OPTIONS)는 모두 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 작성자만 수정/삭제 가능
        return obj.author == request.user

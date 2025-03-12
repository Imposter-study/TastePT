from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("", views.PostViewSet)  # 한 줄로 모든 CRUD API 등록!

urlpatterns = [
    path("upload-image/", views.ImageUploadView.as_view(), name="upload-image"),
    path(
        "comment/<int:pk>/",
        views.CommentUpdateDeleteView.as_view(),
        name="comment-detail",
    ),
    path("", include(router.urls)),
]

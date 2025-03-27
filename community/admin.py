from django.contrib import admin
from .models import Post, Comment, UploadedImage


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    search_fields = ("title", "author", "content")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "author", "post")
    search_fields = ("author", "content")


class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ("image", "uploaded_at")


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UploadedImage, UploadedImageAdmin)

import boto3
import uuid
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def upload_image(image_file, directory="posts"):
    """
    이미지 파일을 업로드하고 URL을 반환하는 유틸리티 함수
    """
    if not image_file:
        return ""

    ext = image_file.name.split(".")[-1] if "." in image_file.name else ""
    safe_filename = f"{uuid.uuid4().hex}.{ext}"

    now = datetime.now()
    relative_path = f"{directory}/{now.year}/{now.month}/{now.day}/{safe_filename}"

    # DEBUG 모드에 따라 저장 로직 분기
    if settings.DEBUG:
        # 로컬 저장소에 저장
        file_path = default_storage.save(relative_path, ContentFile(image_file.read()))
        return settings.MEDIA_URL + file_path
    else:
        # S3에 업로드
        try:
            s3_client = boto3.client(
                "s3",
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

            # S3에 업로드
            s3_client.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                relative_path,
                ExtraArgs={
                    "ContentType": image_file.content_type,
                    "ACL": settings.AWS_DEFAULT_ACL,
                },
            )

            if (
                hasattr(settings, "AWS_S3_CUSTOM_DOMAIN")
                and settings.AWS_S3_CUSTOM_DOMAIN
            ):
                return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{relative_path}"
            else:
                return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{relative_path}"
        except Exception as e:
            raise Exception(f"S3 이미지 업로드 실패: {str(e)}")

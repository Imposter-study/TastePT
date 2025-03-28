# Generated by Django 5.1.7 on 2025-03-27 07:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_alter_user_profile_picture"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(max_length=127, verbose_name="제목")),
                ("message", models.TextField(verbose_name="내용")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="작성일"),
                ),
                (
                    "sent_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="발송일"),
                ),
                (
                    "recipients",
                    models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL, verbose_name="받는사람"
                    ),
                ),
            ],
        ),
    ]

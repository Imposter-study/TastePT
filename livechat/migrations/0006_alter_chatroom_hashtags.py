# Generated by Django 5.1.7 on 2025-03-27 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("livechat", "0005_chatmessage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatroom",
            name="hashtags",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

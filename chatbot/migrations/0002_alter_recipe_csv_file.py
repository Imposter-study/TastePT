# Generated by Django 5.1.7 on 2025-03-13 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="csv_file",
            field=models.FileField(upload_to="csv_file/"),
        ),
    ]

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
import os


file_path = os.path.join(settings.BASE_DIR, "vectors_data")


User = get_user_model()


class Question(models.Model):
    question = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Recipe(models.Model):
    csv_file = models.FileField(upload_to="vectors_data/")
    is_embedded = models.BooleanField(default=False)

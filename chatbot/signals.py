from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Recipe
from .tasks import embed_csv_file

import os
import time

@receiver(post_save, sender=Recipe)
def embed_csv_on_upload(sender, instance, created, **kwargs):
    if created and instance.csv_file:
        # 파일이 실제로 존재하는지 확인
        if os.path.exists(instance.csv_file.path):
            embed_csv_file.delay(instance.id)
        else:            
            time.sleep(1)
            if os.path.exists(instance.csv_file.path):
                embed_csv_file.delay(instance.id)
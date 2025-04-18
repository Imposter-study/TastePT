from celery import shared_task

from .vectorstore import ChromaVectorStore
from .models import Recipe

import time
import os


@shared_task(bind=True, max_retries=5)
def embed_csv_file(self, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.csv_file:
        file_path = recipe.csv_file.path
        for _ in range(3):  
            if os.path.exists(file_path):
                ChromaVectorStore().add_file(file_path=file_path)
                recipe.is_embedded = True
                recipe.save()
                return
            time.sleep(2)

        raise FileNotFoundError(f"CSV 파일이 존재하지 않습니다: {file_path}")
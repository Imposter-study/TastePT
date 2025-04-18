from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Recipe
from .vectorstore import ChromaVectorStore

@receiver(post_save, sender=Recipe)
def embed_csv_on_upload(sender, instance, created, **kwargs):
    if created and instance.csv_file:
        ChromaVectorStore().add_file(file_path=instance.csv_file.path)
        instance.is_embedded = True
        instance.save()
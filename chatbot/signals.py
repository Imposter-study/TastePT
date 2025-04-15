from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Recipe
from .chatbot import VectorStoreManager

@receiver(post_save, sender=Recipe)
def embed_csv_on_upload(sender, instance, created, **kwargs):
    if created and instance.csv_file:
        success = VectorStoreManager().add_file()
        
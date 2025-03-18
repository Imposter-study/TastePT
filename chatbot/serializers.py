from rest_framework import serializers
from .models import Question


class ChatbotSerializer(serializers.Serializer):
    question = serializers.CharField()
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)  
    class Meta:

        model = Question
        fields = ["question", "created_by"]

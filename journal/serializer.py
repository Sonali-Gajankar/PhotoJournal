from rest_framework import serializers
from .models import PhotoJournal


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoJournal
        fields = ["id", "title", "description", "date", "photo"]

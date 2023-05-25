from rest_framework import serializers
from .models import PhotoJournal


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoJournal
        fields = ["title", "description", "date", "photo"]

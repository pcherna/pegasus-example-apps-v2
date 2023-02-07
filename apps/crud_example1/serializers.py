from rest_framework import serializers

from .models import Thing


# Used by the DRF views
class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = ("id", "name", "number", "notes")

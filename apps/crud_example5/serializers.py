from rest_framework import serializers

from .models import SortFilterThing


# Used by the DRF views
class SortFilterThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortFilterThing
        fields = ("id", "name", "number", "notes")

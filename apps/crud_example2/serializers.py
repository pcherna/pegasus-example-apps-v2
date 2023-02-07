from rest_framework import serializers

from .models import TeamThing


# Used by the DRF views
class TeamThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamThing
        fields = ("id", "name", "number", "notes")

from django import forms

from .models import TeamThing


class TeamThingForm(forms.ModelForm):
    class Meta:
        model = TeamThing
        fields = [
            "name",
            "number",
            "notes",
        ]

from django import forms

from .models import InputThing


class InputThingForm(forms.ModelForm):
    class Meta:
        model = InputThing
        fields = [
            "name",
            "birthdate",
            "email",
            "extra",
            "number",
            "notes1",
            "notes2",
            "blocked1",
            "blocked2",
        ]

from django import forms

from .models import PermThing


class PermThingForm(forms.ModelForm):
    class Meta:
        model = PermThing
        fields = [
            "name",
            "number",
            "notes",
        ]

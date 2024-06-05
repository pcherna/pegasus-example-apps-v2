from django import forms

from .models import SortFilterThing


class SortFilterThingForm(forms.ModelForm):
    class Meta:
        model = SortFilterThing
        fields = [
            "name",
            "number",
            "notes",
        ]

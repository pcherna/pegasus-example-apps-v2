from django.db import models
from django.urls import reverse

from apps.teams.models import BaseTeamModel


class InputThing(BaseTeamModel):
    # Some sample fields
    name = models.CharField("Name", max_length=200)
    birthdate = models.CharField("Birthdate", max_length=20)
    email = models.EmailField("Email", blank=True, default="")
    extra = models.BooleanField("Extra Stuff", default=True)
    number = models.IntegerField("Number", default=0)
    notes1 = models.TextField("Notes 1", max_length=4096, blank=True, default="")
    notes2 = models.TextField("Notes 2", max_length=4096, blank=True, default="")
    blocked1 = models.CharField("Blocked 1", max_length=200, blank=True, default="You cannot set this")
    blocked2 = models.CharField("Blocked 2", max_length=200, blank=True, default="You cannot set this either")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud_example4:inputthing_detail", kwargs={"team_slug": self.team.slug, "pk": self.pk})

    class Meta:
        ordering = ["name"]

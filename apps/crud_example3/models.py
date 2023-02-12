from django.db import models
from django.urls import reverse

from apps.teams.models import BaseTeamModel


class PermThing(BaseTeamModel):
    # Some sample fields
    name = models.CharField("Name", max_length=200)
    number = models.IntegerField("Number", default=0)
    notes = models.TextField("Notes", max_length=4096, blank=True, default="")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud_example3:permthing_detail", kwargs={"team_slug": self.team.slug, "pk": self.pk})

    class Meta:
        ordering = ["name"]
        # In addition to the standard "view_permthing", "change_permthing", "add_permthing", and "delete_permthing"
        # permissions, let's make a custom one that will mean user can only see the summary-info about these objects
        permissions = [
            ("view_summary_permthing", "Can view only the summary info about a perm thing"),
        ]

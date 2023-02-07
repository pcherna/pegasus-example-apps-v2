from django.db import models
from django.urls import reverse

from apps.utils.models import BaseModel


class Thing(BaseModel):
    # Some sample fields
    name = models.CharField("Name", max_length=200)
    number = models.IntegerField("Number", default=0)
    notes = models.TextField("Notes", max_length=4096, blank=True, default="")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crud_example1:thing_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["name"]

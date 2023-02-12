from django.contrib import admin
from .models import InputThing


@admin.register(InputThing)
class InputThingAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ["name", "number"]
    # Filters to include in admin's list view
    list_filter = ["team"]

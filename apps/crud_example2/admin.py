from django.contrib import admin
from .models import TeamThing


@admin.register(TeamThing)
class TeamThingAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ["name", "number"]
    # Filters to include in admin's list view
    list_filter = ["team"]

from django.contrib import admin
from .models import PermThing


@admin.register(PermThing)
class PermThingAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ["name", "number"]
    # Filters to include in admin's list view
    list_filter = ["team"]

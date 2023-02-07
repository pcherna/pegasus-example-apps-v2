from django.contrib import admin
from .models import Thing


@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    # Fields to include in admin's list view
    list_display = ["name", "number"]

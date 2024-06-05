from django_filters import rest_framework as filters

from .models import SortFilterThing


class SortFilterThingFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains", label="Name Contains")
    number = filters.NumberFilter(label="Number Is")
    # ZZZ: Example of a ChoiceFilter, to add later
    # display_status = filters.ChoiceFilter(choices=DISPLAY_STATUS_CHOICES, method="filter_display_status")
    sort = filters.OrderingFilter(
        # Map of "field-name", "query-param name" of things that are orderable
        fields=(
            ("name", "name"),
            ("number", "number"),
        ),
    )

    class Meta:
        model = SortFilterThing
        fields = ["name", "number"]

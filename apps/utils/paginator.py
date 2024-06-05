from django.core.paginator import Paginator, PageNotAnInteger


class ClampingPaginator(Paginator):
    """Paginator that clamps the max pages insteads of throwing an error.
    If we are on a high numbered page, then apply a filter, we could find ourselves
    "past the end", and it's better to clamp than to error."""
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)

    def validate_number(self, number):
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number > self.num_pages:
            number = self.num_pages
        return super().validate_number(number)

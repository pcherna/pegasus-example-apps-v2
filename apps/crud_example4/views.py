from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.teams.mixins import LoginAndTeamRequiredMixin

from .forms import InputThingForm
from .models import InputThing

# --------------------------------------------------------------------------------

# A reasonable value for pagination would be 10 or 20 entries per page.
# Here we use 4 (a very low value), so we can show off the pagination using fewer items
PAGINATE_BY = 4
# For pagination, we use get_elided_page_range() to give a list of pages that always has some
# pages at the beginning and end, and some on either side of current, with ellipsis where needed.

# --------------------------------------------------------------------------------

# InputThing (team-specific CRUD example) Class-Based View implementation


class InputThingDetailView(LoginAndTeamRequiredMixin, DetailView):
    """Class-Based View to see InputThing details."""

    model = InputThing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "InputThings" in the nav-bar
        context["active_tab"] = "crud_example4"
        return context


class InputThingCreateView(LoginAndTeamRequiredMixin, CreateView):
    """Class-Based View to create a InputThing."""

    model = InputThing
    form_class = InputThingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "InputThings" in the nav-bar
        context["active_tab"] = "crud_example4"
        return context

    def form_valid(self, form):
        form.instance.team = self.request.team
        return super().form_valid(form)


class InputThingUpdateView(LoginAndTeamRequiredMixin, UpdateView):
    """Class-Based View to update a InputThing."""

    model = InputThing
    form_class = InputThingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "InputThings" in the nav-bar
        context["active_tab"] = "crud_example4"
        return context


class InputThingDeleteView(LoginAndTeamRequiredMixin, DeleteView):
    """Class-Based View to delete a InputThing."""

    model = InputThing

    def get_success_url(self):
        return reverse_lazy("crud_example4:inputthing_list", kwargs={"team_slug": self.request.team.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "InputThings" in the nav-bar
        context["active_tab"] = "crud_example4"
        return context


class InputThingListHtmxView(LoginAndTeamRequiredMixin, ListView):
    """Enhanced Class-Based View list of InputThings.
    Uses htmx to implement pagination with clean visuals when updating.
    We configure a single URL endpoint to use for both the full-page render, and the htmx update
    (see get_template_names())
    """

    model = InputThing
    paginate_by = PAGINATE_BY
    template_name = "crud_example4/inputthing_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "InputThings" in the nav-bar
        context["active_tab"] = "crud_example4"
        page = context["page_obj"]
        # list() realizes the iterator into a list, so we can twice if desired (above and below list)
        context["elided_page_range"] = list(
            page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        )
        return context

    def get_template_names(self):
        """If we are receiving an htmx request, return just the partial, else the whole page."""
        if "HX-Request" in self.request.headers:
            return ["crud_example4/inputthing_list_htmx_partial.html"]
        else:
            # Use the full template
            return ["crud_example4/inputthing_list_htmx.html"]

from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from rest_framework import viewsets

from apps.crud_example5.filters import SortFilterThingFilter
from apps.teams.decorators import login_and_team_required
from apps.teams.mixins import LoginAndTeamRequiredMixin
from apps.utils.paginator import ClampingPaginator

from .forms import SortFilterThingForm
from .models import SortFilterThing
from .serializers import SortFilterThingSerializer

# --------------------------------------------------------------------------------

# A reasonable value for pagination would be 10 or 20 entries per page.
# Here we use 4 (a very low value), so we can show off the pagination using fewer items
PAGINATE_BY = 4
# For pagination, we use get_elided_page_range() to give a list of pages that always has some
# pages at the beginning and end, and some on either side of current, with ellipsis where needed.

# --------------------------------------------------------------------------------

# SortFilterThing (team-specific CRUD example) Function-Based View implementation


@login_and_team_required
def sortfilterthing_list_view(request, team_slug):
    """Function-Based View list of SortFilterThings."""
    context = {}

    # Filter the set of objects to view to only show this team's objects
    sortfilterthing_list = SortFilterThing.objects.filter(team=request.team)

    paginator = Paginator(sortfilterthing_list, PAGINATE_BY)
    page = request.GET.get("page", 1)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
    context["active_tab"] = "crud_example5"
    context["page_obj"] = page
    context["object_list"] = page.object_list
    context["is_paginated"] = page.has_other_pages
    context["elided_page_range"] = list(paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1))
    return render(request, "crud_example5/sortfilterthing_list.html", context)


@login_and_team_required
def sortfilterthing_detail_view(request, team_slug, pk):
    """Function-Based View to see SortFilterThing details."""
    context = {}
    # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
    context["active_tab"] = "crud_example5"
    # Allow only if object belongs to this team
    context["object"] = get_object_or_404(SortFilterThing, id=pk, team=request.team)
    return render(request, "crud_example5/sortfilterthing_detail.html", context)


@login_and_team_required
def sortfilterthing_create_view(request, team_slug):
    """Function-Based View to create a SortFilterThing."""
    context = {}
    form = SortFilterThingForm(request.POST or None)
    if form.is_valid():
        new_object = form.save(commit=False)
        # Add my team to the object
        new_object.team = request.team
        new_object.save()
        return HttpResponseRedirect(
            reverse("crud_example5:sortfilterthing_detail", kwargs={"team_slug": team_slug, "pk": new_object.id})
        )
    # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
    context["active_tab"] = "crud_example5"
    context["form"] = form
    return render(request, "crud_example5/sortfilterthing_form.html", context)


@login_and_team_required
def sortfilterthing_update_view(request, team_slug, pk):
    """Function-Based View to update a SortFilterThing."""
    context = {}
    # Allow only if object belongs to this team
    obj = get_object_or_404(SortFilterThing, id=pk, team=request.team)
    form = SortFilterThingForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse("crud_example5:sortfilterthing_detail", kwargs={"team_slug": team_slug, "pk": pk})
        )
    # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
    context["active_tab"] = "crud_example5"
    context["form"] = form
    context["team"] = request.team
    context["object"] = obj
    return render(request, "crud_example5/sortfilterthing_form.html", context)


@login_and_team_required
def sortfilterthing_delete_view(request, team_slug, pk):
    """Function-Based View to delete a SortFilterThing."""
    # Allow only if object belongs to this team
    obj = get_object_or_404(SortFilterThing, id=pk, team=request.team)
    obj.delete()
    return HttpResponseRedirect(reverse("crud_example5:sortfilterthing_list", kwargs={"team_slug": team_slug}))


# --------------------------------------------------------------------------------

# SortFilterThing (team-specific CRUD example) Class-Based View implementation


class SortFilterThingDetailView(LoginAndTeamRequiredMixin, DetailView):
    """Class-Based View to see SortFilterThing details."""

    model = SortFilterThing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
        context["active_tab"] = "crud_example5"
        return context


class SortFilterThingCreateView(LoginAndTeamRequiredMixin, CreateView):
    """Class-Based View to create a SortFilterThing."""

    model = SortFilterThing
    form_class = SortFilterThingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
        context["active_tab"] = "crud_example5"
        return context

    def form_valid(self, form):
        form.instance.team = self.request.team
        return super().form_valid(form)


class SortFilterThingUpdateView(LoginAndTeamRequiredMixin, UpdateView):
    """Class-Based View to update a SortFilterThing."""

    model = SortFilterThing
    form_class = SortFilterThingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
        context["active_tab"] = "crud_example5"
        return context


class SortFilterThingDeleteView(LoginAndTeamRequiredMixin, DeleteView):
    """Class-Based View to delete a SortFilterThing."""

    model = SortFilterThing

    def get_success_url(self):
        return reverse_lazy("crud_example5:sortfilterthing_list", kwargs={"team_slug": self.request.team.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
        context["active_tab"] = "crud_example5"
        return context


class SortFilterThingListHtmxView(LoginAndTeamRequiredMixin, ListView):
    """Enhanced Class-Based View list of SortFilterThings.
    Uses htmx to implement pagination with clean visuals when updating.
    We configure a single URL endpoint to use for both the full-page render, and the htmx update
    (see get_template_names())
    """

    model = SortFilterThing
    paginate_by = PAGINATE_BY
    # Filtering can reduce the matches so that the current page is off the end, ClampingPaginator keeps us in range
    paginator_class = ClampingPaginator
    template_name = "crud_example5/sortfilterthing_list.html"

    def get_queryset(self):
        print("SortFilterThingListHtmxView.get_queryset()")
        qs = super().get_queryset()
        self.total_count = qs.count
        self.filter = SortFilterThingFilter(self.request.GET, request=self.request, queryset=qs)
        self.filtered_count = self.filter.qs.count
        return self.filter.qs

    def get_context_data(self, **kwargs):
        print("SortFilterThingListHtmxView.get_context_data()")
        context = super().get_context_data(**kwargs)
        page = context["page_obj"]
        context.update(
            {
                # Lets crud_example_nav.html highlight "SortFilterThings" in the nav-bar
                "active_tab": "crud_example5",
                # list()ify the iterator, so we can reference it twice if desired (above and below list)
                "elided_page_range": list(page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)),
                # Filter info
                "filter": self.filter,
                "total_count": self.total_count,
                "filtered_count": self.filtered_count,
                # ZZZ: Copied over, do I need this?
                # If this is a partial update of the object-list
                "hx_target_object_list": self.request.htmx.target == "object-list",
            }
        )
        return context

    def get_template_names(self):
        """If we are receiving an htmx request for the object-list, return the
        corresponding partial template, else the whole-page template."""
        if self.request.htmx.target == "object-list":
            return ["crud_example5/sortfilterthing_list_objects.html"]
        else:
            # Use the full template
            return ["crud_example5/sortfilterthing_list.html"]


# --------------------------------------------------------------------------------

# SortFilterThing (team-specific CRUD example) DRF views


class SortFilterThingViewSet(viewsets.ModelViewSet):
    """Class-Based ViewSet for REST API access to SortFilterThings."""

    serializer_class = SortFilterThingSerializer
    queryset = SortFilterThing.objects.all()

    def get_queryset(self):
        qs = super().get_queryset().filter(team=self.request.team)
        return qs

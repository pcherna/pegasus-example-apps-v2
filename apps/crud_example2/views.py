from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from rest_framework import viewsets

from apps.teams.decorators import login_and_team_required
from apps.teams.mixins import LoginAndTeamRequiredMixin

from .forms import TeamThingForm
from .models import TeamThing
from .serializers import TeamThingSerializer

# --------------------------------------------------------------------------------

# A reasonable value for pagination would be 10 or 20 entries per page.
# Here we use 4 (a very low value), so we can show off the pagination using fewer items
PAGINATE_BY = 4
# For pagination, we use get_elided_page_range() to give a list of pages that always has some
# pages at the beginning and end, and some on either side of current, with ellipsis where needed.

# --------------------------------------------------------------------------------

# TeamThing (team-specific CRUD example) Function-Based View implementation


@login_and_team_required
def teamthing_list_view(request, team_slug):
    """Function-Based View list of TeamThings."""
    context = {}

    # Filter the set of objects to view to only show this team's objects
    teamthing_list = TeamThing.objects.filter(team=request.team)

    paginator = Paginator(teamthing_list, PAGINATE_BY)
    page = request.GET.get("page", 1)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
    context["active_tab"] = "crud_example2"
    context["page_obj"] = page
    context["object_list"] = page.object_list
    context["is_paginated"] = page.has_other_pages
    context["elided_page_range"] = list(paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1))
    return render(request, "crud_example2/teamthing_list.html", context)


@login_and_team_required
def teamthing_detail_view(request, team_slug, pk):
    """Function-Based View to see TeamThing details."""
    context = {}
    # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
    context["active_tab"] = "crud_example2"
    # Allow only if object belongs to this team
    context["object"] = get_object_or_404(TeamThing, id=pk, team=request.team)
    return render(request, "crud_example2/teamthing_detail.html", context)


@login_and_team_required
def teamthing_create_view(request, team_slug):
    """Function-Based View to create a TeamThing."""
    context = {}
    form = TeamThingForm(request.POST or None)
    if form.is_valid():
        new_object = form.save(commit=False)
        # Add my team to the object
        new_object.team = request.team
        new_object.save()
        return HttpResponseRedirect(
            reverse("crud_example2:teamthing_detail", kwargs={"team_slug": team_slug, "pk": new_object.id})
        )
    # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
    context["active_tab"] = "crud_example2"
    context["form"] = form
    return render(request, "crud_example2/teamthing_form.html", context)


@login_and_team_required
def teamthing_update_view(request, team_slug, pk):
    """Function-Based View to update a TeamThing."""
    context = {}
    # Allow only if object belongs to this team
    obj = get_object_or_404(TeamThing, id=pk, team=request.team)
    form = TeamThingForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse("crud_example2:teamthing_detail", kwargs={"team_slug": team_slug, "pk": pk})
        )
    # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
    context["active_tab"] = "crud_example2"
    context["form"] = form
    context["team"] = request.team
    context["object"] = obj
    return render(request, "crud_example2/teamthing_form.html", context)


@login_and_team_required
def teamthing_delete_view(request, team_slug, pk):
    """Function-Based View to delete a TeamThing."""
    # Allow only if object belongs to this team
    obj = get_object_or_404(TeamThing, id=pk, team=request.team)
    obj.delete()
    return HttpResponseRedirect(reverse("crud_example2:teamthing_list", kwargs={"team_slug": team_slug}))


# --------------------------------------------------------------------------------

# TeamThing (team-specific CRUD example) Class-Based View implementation


class TeamThingListView(LoginAndTeamRequiredMixin, ListView):
    """Class-Based View list of TeamThings."""

    model = TeamThing
    paginate_by = PAGINATE_BY
    template_name = "crud_example2/teamthing_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
        context["active_tab"] = "crud_example2"
        page = context["page_obj"]
        # list() realizes the iterator into a list, so we can twice if desired (above and below list)
        context["elided_page_range"] = list(
            page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        )
        return context


class TeamThingDetailView(LoginAndTeamRequiredMixin, DetailView):
    """Class-Based View to see TeamThing details."""

    model = TeamThing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
        context["active_tab"] = "crud_example2"
        return context


class TeamThingCreateView(LoginAndTeamRequiredMixin, CreateView):
    """Class-Based View to create a TeamThing."""

    model = TeamThing
    form_class = TeamThingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
        context["active_tab"] = "crud_example2"
        return context

    def form_valid(self, form):
        form.instance.team = self.request.team
        return super().form_valid(form)


class TeamThingUpdateView(LoginAndTeamRequiredMixin, UpdateView):
    """Class-Based View to update a TeamThing."""

    model = TeamThing
    form_class = TeamThingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
        context["active_tab"] = "crud_example2"
        return context


class TeamThingDeleteView(LoginAndTeamRequiredMixin, DeleteView):
    """Class-Based View to delete a TeamThing."""

    model = TeamThing

    def get_success_url(self):
        return reverse_lazy("crud_example2:teamthing_list", kwargs={"team_slug": self.request.team.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
        context["active_tab"] = "crud_example2"
        return context


class TeamThingListHtmxView(LoginAndTeamRequiredMixin, ListView):
    """Enhanced Class-Based View list of TeamThings.
    Uses htmx to implement pagination with clean visuals when updating.
    We configure a single URL endpoint to use for both the full-page render, and the htmx update
    (see get_template_names())
    """

    model = TeamThing
    paginate_by = PAGINATE_BY
    template_name = "crud_example2/teamthing_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "TeamThings" in the nav-bar
        context["active_tab"] = "crud_example2"
        page = context["page_obj"]
        # list() realizes the iterator into a list, so we can twice if desired (above and below list)
        context["elided_page_range"] = list(
            page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        )
        return context

    def get_template_names(self):
        """If we are receiving an htmx request, return just the partial, else the whole page."""
        if "HX-Request" in self.request.headers:
            return ["crud_example2/teamthing_list_htmx_partial.html"]
        else:
            # Use the full template
            return ["crud_example2/teamthing_list_htmx.html"]

    def dispatch(self, request, *args, **kwargs):
        """Since this view returns different results when it's an HTMX (partial) versus full request,
        Let the browser know to cache those things differently."""
        response = super().dispatch(request, *args, **kwargs)
        # Use HTTP "Vary" response header to tell the browser cache that the response can differ
        # based on the values in HX-Request, and not to fold things into the same cache
        # See https://htmx.org/docs/#caching and https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching#vary
        response["Vary"] = "HX-Request"
        return response


# --------------------------------------------------------------------------------

# TeamThing (team-specific CRUD example) DRF views


class TeamThingViewSet(viewsets.ModelViewSet):
    """Class-Based ViewSet for REST API access to TeamThings."""

    serializer_class = TeamThingSerializer
    queryset = TeamThing.objects.all()

    def get_queryset(self):
        qs = super().get_queryset().filter(team=self.request.team)
        return qs

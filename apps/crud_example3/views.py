from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apps.teams.decorators import login_and_team_required
from apps.teams.mixins import LoginAndTeamRequiredMixin

from .forms import PermThingForm
from .models import PermThing

# --------------------------------------------------------------------------------

# A reasonable value for pagination would be 10 or 20 entries per page.
# Here we use 4 (a very low value), so we can show off the pagination using fewer items
PAGINATE_BY = 4
# For pagination, we use get_elided_page_range() to give a list of pages that always has some
# pages at the beginning and end, and some on either side of current, with ellipsis where needed.

# --------------------------------------------------------------------------------


perms = [
    "view_summary_permthing",
    "view_permthing",
    "change_permthing",
    "add_permthing",
    "delete_permthing",
]


@login_and_team_required
def permthing_set_perms_view(request, team_slug, perm_level):
    """Function-Based View to change the user's permissions."""
    # If this is our first time through, let's create a Group to hold the permissions
    print(f"In permthing_set_perms_view. level {perm_level}")
    group_name = "Demo Permissions Group"
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        group = Group(name=group_name)
        group.save()
        print(f"Created Group {group_name}")
    # And add the current user to the group
    request.user.groups.add(group)

    ct = ContentType.objects.filter(app_label="crud_example3").get(model="permthing")
    print(f"{ct=}")
    for p in Permission.objects.filter(content_type_id=ct):
        if perm_level > perms.index(p.codename):
            print(f"  Adding {p.codename}")
            group.permissions.add(p)
        else:
            print(f"  Removing {p.codename}")
            group.permissions.remove(p)

    return HttpResponseRedirect(
        "", headers={"HX-Redirect": reverse("crud_example3:permthing_list", kwargs={"team_slug": team_slug})}
    )


# --------------------------------------------------------------------------------

# PermThing (team-specific CRUD example) Function-Based View implementation


# Note: This view should in theory require crud_example3.view_summary_permthing permission, however the
# demo controls for setting permissions are on the page itself, so we need to always offer this view
@login_and_team_required
def permthing_list_view(request, team_slug):
    """Function-Based View list of PermThings."""
    context = {}

    # Filter the set of objects to view to only show this team's objects
    permthing_list = PermThing.objects.filter(team=request.team)

    paginator = Paginator(permthing_list, PAGINATE_BY)
    page = request.GET.get("page", 1)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
    context["active_tab"] = "crud_example3"
    context["page_obj"] = page
    context["object_list"] = page.object_list
    context["is_paginated"] = page.has_other_pages
    context["elided_page_range"] = list(paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1))
    return render(request, "crud_example3/permthing_list.html", context)


@permission_required("crud_example3.view_permthing", raise_exception=True)
@login_and_team_required
def permthing_detail_view(request, team_slug, pk):
    """Function-Based View to see PermThing details."""
    context = {}
    # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
    context["active_tab"] = "crud_example3"
    # Allow only if object belongs to this team
    context["object"] = get_object_or_404(PermThing, id=pk, team=request.team)
    return render(request, "crud_example3/permthing_detail.html", context)


@permission_required("crud_example3.add_permthing", raise_exception=True)
@login_and_team_required
def permthing_create_view(request, team_slug):
    """Function-Based View to create a PermThing."""
    context = {}
    form = PermThingForm(request.POST or None)
    if form.is_valid():
        new_object = form.save(commit=False)
        # Add my team to the object
        new_object.team = request.team
        new_object.save()
        return HttpResponseRedirect(
            reverse("crud_example3:permthing_detail", kwargs={"team_slug": team_slug, "pk": new_object.id})
        )
    # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
    context["active_tab"] = "crud_example3"
    context["form"] = form
    return render(request, "crud_example3/permthing_form.html", context)


@permission_required("crud_example3.change_permthing", raise_exception=True)
@login_and_team_required
def permthing_update_view(request, team_slug, pk):
    """Function-Based View to update a PermThing."""
    context = {}
    # Allow only if object belongs to this team
    obj = get_object_or_404(PermThing, id=pk, team=request.team)
    form = PermThingForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(
            reverse("crud_example3:permthing_detail", kwargs={"team_slug": team_slug, "pk": pk})
        )
    # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
    context["active_tab"] = "crud_example3"
    context["form"] = form
    context["team"] = request.team
    context["object"] = obj
    return render(request, "crud_example3/permthing_form.html", context)


@permission_required("crud_example3.delete_permthing", raise_exception=True)
@login_and_team_required
def permthing_delete_view(request, team_slug, pk):
    """Function-Based View to delete a PermThing."""
    # Allow only if object belongs to this team
    obj = get_object_or_404(PermThing, id=pk, team=request.team)
    obj.delete()
    return HttpResponseRedirect(reverse("crud_example3:permthing_list", kwargs={"team_slug": team_slug}))


# --------------------------------------------------------------------------------

# PermThing (team-specific CRUD example) Class-Based View implementation


class PermThingDetailView(LoginAndTeamRequiredMixin, UserPassesTestMixin, DetailView):
    """Class-Based View to see PermThing details."""

    model = PermThing

    def test_func(self):
        return self.request.user.has_perm("crud_example3.view_permthing")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
        context["active_tab"] = "crud_example3"
        return context


class PermThingCreateView(LoginAndTeamRequiredMixin, UserPassesTestMixin, CreateView):
    """Class-Based View to create a PermThing."""

    model = PermThing
    form_class = PermThingForm

    def test_func(self):
        return self.request.user.has_perm("crud_example3.add_permthing")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
        context["active_tab"] = "crud_example3"
        return context

    def form_valid(self, form):
        form.instance.team = self.request.team
        return super().form_valid(form)


class PermThingUpdateView(LoginAndTeamRequiredMixin, UserPassesTestMixin, UpdateView):
    """Class-Based View to update a PermThing."""

    model = PermThing
    form_class = PermThingForm

    def test_func(self):
        return self.request.user.has_perm("crud_example3.change_permthing")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
        context["active_tab"] = "crud_example3"
        return context


class PermThingDeleteView(LoginAndTeamRequiredMixin, UserPassesTestMixin, DeleteView):
    """Class-Based View to delete a PermThing."""

    model = PermThing

    def test_func(self):
        return self.request.user.has_perm("crud_example3.delete_permthing")

    def get_success_url(self):
        return reverse_lazy("crud_example3:permthing_list", kwargs={"team_slug": self.request.team.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
        context["active_tab"] = "crud_example3"
        return context


# Note: This view should in theory require crud_example3.view_summary_permthing permission, however the
# demo controls for setting permissions are on the page itself, so we need to always offer this view
class PermThingListHtmxView(LoginAndTeamRequiredMixin, ListView):
    """Enhanced Class-Based View list of PermThings.
    Uses htmx to implement pagination with clean visuals when updating.
    We configure a single URL endpoint to use for both the full-page render, and the htmx update
    (see get_template_names())
    """

    model = PermThing
    paginate_by = PAGINATE_BY
    template_name = "crud_example3/permthing_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lets crud_example_nav.html highlight "PermThings" in the nav-bar
        context["active_tab"] = "crud_example3"
        page = context["page_obj"]
        # list() realizes the iterator into a list, so we can twice if desired (above and below list)
        context["elided_page_range"] = list(
            page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        )
        return context

    def get_template_names(self):
        """If we are receiving an htmx request for the object-list, return the
        corresponding partial template, else the whole-page template."""
        if self.request.htmx.target == "object-list":
            return ["crud_example3/permthing_list_htmx_partial.html"]
        else:
            # Use the full template
            return ["crud_example3/permthing_list_htmx.html"]

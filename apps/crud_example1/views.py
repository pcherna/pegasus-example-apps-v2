from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from rest_framework import viewsets

from .forms import ThingForm
from .models import Thing
from .serializers import ThingSerializer

# --------------------------------------------------------------------------------

# A reasonable value for pagination would be 10 or 20 entries per page.
# Here we use 4 (a very low value), so we can show off the pagination using fewer items
PAGINATE_BY = 4
# For pagination, we use get_elided_page_range() to give a list of pages that always has some
# pages at the beginning and end, and some on either side of current, with ellipsis where needed.

# --------------------------------------------------------------------------------

# Thing (non-team-specific CRUD example) Function-Based View implementation


@login_required
def thing_list_view(request):
    """Function-Based View list of Things."""
    context = {}

    thing_list = Thing.objects.all()

    paginator = Paginator(thing_list, PAGINATE_BY)
    page = request.GET.get("page", 1)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Lets crud_example_nav.html highlight "Things" in the nav-bar
    context["active_tab"] = "crud_example1"
    context["page_obj"] = page
    context["object_list"] = page.object_list
    context["is_paginated"] = page.has_other_pages
    context["elided_page_range"] = list(paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1))
    return render(request, "crud_example1/thing_list.html", context)


@login_required
def thing_detail_view(request, pk):
    """Function-Based View to see Thing details."""
    context = {}
    # Lets crud_example_nav.html highlight "Things" in the nav-bar
    context["active_tab"] = "crud_example1"
    context["object"] = Thing.objects.get(id=pk)
    return render(request, "crud_example1/thing_detail.html", context)


@login_required
def thing_create_view(request):
    """Function-Based View to create a Thing."""
    context = {}
    form = ThingForm(request.POST or None)
    if form.is_valid():
        saved_form = form.save()
        return HttpResponseRedirect(reverse("crud_example1:thing_detail", kwargs={"pk": saved_form.id}))
    # Lets crud_example_nav.html highlight "Things" in the nav-bar
    context["active_tab"] = "crud_example1"
    context["form"] = form
    return render(request, "crud_example1/thing_form.html", context)


@login_required
def thing_update_view(request, pk):
    """Function-Based View to update a Thing."""
    context = {}
    obj = get_object_or_404(Thing, id=pk)
    form = ThingForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("crud_example1:thing_detail", kwargs={"pk": pk}))
    # Lets crud_example_nav.html highlight "Things" in the nav-bar
    context["active_tab"] = "crud_example1"
    context["form"] = form
    context["object"] = obj
    return render(request, "crud_example1/thing_form.html", context)


@login_required
def thing_delete_view(request, pk):
    """Function-Based View to delete a Thing."""
    obj = get_object_or_404(Thing, id=pk)
    obj.delete()
    return HttpResponseRedirect(reverse("crud_example1:thing_list"))


# --------------------------------------------------------------------------------

# Thing (non-team-specific CRUD example) Class-Based View implementation


class ThingListView(LoginRequiredMixin, ListView):
    """Class-Based View list of Things."""

    model = Thing
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "crud_example1"
        page = context["page_obj"]
        # list() realizes the iterator into a list, so we can twice if desired (above and below list)
        context["elided_page_range"] = list(
            page.paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
        )
        return context


class ThingDetailView(LoginRequiredMixin, DetailView):
    """Class-Based View to see Thing details."""

    model = Thing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "crud_example1"
        return context


class ThingCreateView(LoginRequiredMixin, CreateView):
    """Class-Based View to create a Thing."""

    model = Thing
    form_class = ThingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "crud_example1"
        return context


class ThingUpdateView(LoginRequiredMixin, UpdateView):
    """Class-Based View to update a Thing."""

    model = Thing
    form_class = ThingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "crud_example1"
        return context


class ThingDeleteView(LoginRequiredMixin, DeleteView):
    """Class-Based View to delete a Thing."""

    model = Thing
    success_url = reverse_lazy("crud_example1:thing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "crud_example1"
        return context


class ThingListHtmxView(LoginRequiredMixin, ListView):
    """Enhanced Class-Based View list of Things.
    Uses htmx to implement pagination with clean visuals when updating.
    We configure a single URL endpoint to use for both the full-page render, and the htmx update
    (see get_template_names())
    """

    model = Thing
    paginate_by = PAGINATE_BY

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active_tab"] = "crud_example1"
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
            return ["crud_example1/thing_list_htmx_partial.html"]
        else:
            # Use the full template
            return ["crud_example1/thing_list_htmx.html"]


# --------------------------------------------------------------------------------

# Thing (non-team-specific CRUD example) DRF views


class ThingViewSet(viewsets.ModelViewSet):
    """Class-Based ViewSet for REST API access to Things."""

    serializer_class = ThingSerializer
    queryset = Thing.objects.all()

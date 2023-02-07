from django.urls import path
from rest_framework import routers

from . import views


app_name = "crud_example1"

urlpatterns = [
    #
    # URL paths for the Function-Based View implementation
    #
    path("", views.thing_list_view, name="thing_list"),
    path("<int:pk>/", views.thing_detail_view, name="thing_detail"),
    path("new/", views.thing_create_view, name="thing_create"),
    path("<int:pk>/update/", views.thing_update_view, name="thing_update"),
    path("<int:pk>/delete/", views.thing_delete_view, name="thing_delete"),
    #
    # URL paths for the Class-Based View implementation
    #
    # path("", views.ThingListView.as_view(), name="thing_list"),
    # path("<int:pk>/", views.ThingDetailView.as_view(), name="thing_detail"),
    # path("new/", views.ThingCreateView.as_view(), name="thing_create"),
    # path("<int:pk>/update/", views.ThingUpdateView.as_view(), name="thing_update"),
    # path("<int:pk>/delete/", views.ThingDeleteView.as_view(), name="thing_delete"),
    #
    #  URL path for the htmx pagination implementation of a CBV list
    #
    # path("", views.ThingListHtmxView.as_view(), name="thing_list"),
]

# drf config
router = routers.DefaultRouter()
router.register("api/things", views.ThingViewSet)

urlpatterns += router.urls
